#!/usr/bin/env python3
"""Fraud Shield – Flask web app.

Endpoints:
- `/`            → Landing page (static)
- `/analyze`     → CSV upload form
- `/predict`     → Handle upload, run model, render results
- `/download/<token>` → One-time CSV download

Loads a model from `config.MODEL_PATHS` and uses helpers in `utils.py`.
"""
from __future__ import annotations

import io
import os
import secrets
from pathlib import Path
from typing import Optional, Dict, Any

from flask import (
    Flask, request, render_template, send_file, redirect, url_for, flash
)
import pandas as pd
import numpy as np
import joblib

from config import MODEL_PATHS, UI_CONFIG
from utils import (
    validate_csv_data,
    prepare_data_for_prediction,
    calculate_risk_metrics,
    generate_summary_report,
    create_prediction_visualizations,
)
import plotly.io as pio

BASE_DIR = Path(__file__).parent
app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "website"),
    template_folder=str(BASE_DIR / "templates"),
    static_url_path="/"
)
app.config.update(
    SECRET_KEY=os.environ.get("FRAUD_SHIELD_SECRET", secrets.token_hex(16))
)

RESULTS_STORE: Dict[str, bytes] = {}


def load_model_with_fallback() -> tuple[Optional[object], Optional[str]]:
    """Return the first valid model found and its path, otherwise (None, None)."""
    for path in MODEL_PATHS:
        try:
            p = Path(path)
            if p.exists():
                model = joblib.load(p)
                if hasattr(model, "predict"):
                    return model, str(p)
        except Exception:
            pass
    return None, None

MODEL, MODEL_PATH = load_model_with_fallback()


@app.route("/")
def home():
    """Serve the landing page."""
    index_path = BASE_DIR / "website" / "index.html"
    return send_file(str(index_path))

@app.route("/app.js")
def app_js():
    """Serve the JavaScript file."""
    js_path = BASE_DIR / "website" / "app.js"
    if js_path.exists():
        return send_file(str(js_path), mimetype="application/javascript")
    return "", 404


@app.route("/analyze", methods=["GET"])
def analyze():
    return render_template(
        "analyze.html",
        model_path=MODEL_PATH,
        page_title=UI_CONFIG.get("page_title", "Fraud Shield")
    )


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        flash("No file part in request", "danger")
        return redirect(url_for("analyze"))

    file = request.files.get("file")
    if not file or file.filename == "":
        flash("No file selected", "warning")
        return redirect(url_for("analyze"))

    if MODEL is None:
        flash("Model not available. Please add a trained model file.", "danger")
        return redirect(url_for("analyze"))

    try:
        df = pd.read_csv(file)
    except Exception as e:
        flash(f"Failed to read CSV: {e}", "danger")
        return redirect(url_for("analyze"))

    is_valid, error_message = validate_csv_data(df)
    if not is_valid:
        flash(f"Data validation failed: {error_message}", "danger")
        return redirect(url_for("analyze"))

    features_df, actual_labels = prepare_data_for_prediction(df)

    try:
        predictions = MODEL.predict(features_df)
        proba = None
        if hasattr(MODEL, "predict_proba"):
            try:
                probs = MODEL.predict_proba(features_df)
                if isinstance(probs, np.ndarray) and probs.ndim == 2 and probs.shape[1] >= 2:
                    proba = probs[:, 1]
            except Exception:
                proba = None
    except Exception as e:
        flash(f"Model prediction failed: {e}", "danger")
        return redirect(url_for("analyze"))

    metrics = calculate_risk_metrics(predictions, proba)
    results_df = df.copy()
    results_df['Fraud Prediction'] = predictions
    results_df['Fraud Prediction'] = results_df['Fraud Prediction'].map({0: 'Legitimate', 1: 'Fraudulent'})
    if proba is not None:
        results_df['Fraud Probability'] = proba

    csv_bytes = results_df.to_csv(index=False).encode("utf-8")
    token = secrets.token_urlsafe(16)
    RESULTS_STORE[token] = csv_bytes

    summary = generate_summary_report(metrics, MODEL_PATH or "Unknown")

    figures = create_prediction_visualizations(metrics, proba)
    
    # Configure Plotly for responsive charts
    plotly_config = {
        'displayModeBar': True, 
        'displaylogo': False,
        'responsive': True,
        'autosize': True,
        'useResizeHandler': True
    }
    
    dist_html = pio.to_html(
        figures["distribution"],
        include_plotlyjs='cdn',
        full_html=False,
        config=plotly_config
    )
    if "probabilities" in figures:
        right_fig = figures["probabilities"]
    else:
        right_fig = figures["counts"]
    right_html = pio.to_html(
        right_fig,
        include_plotlyjs=False,
        full_html=False,
        config=plotly_config
    )

    return render_template(
        "results.html",
        metrics=metrics,
        row_count=len(results_df),
        download_token=token,
        model_path=MODEL_PATH,
        summary=summary,
        dist_html=dist_html,
        right_html=right_html,
        page_title=UI_CONFIG.get("page_title", "Fraud Shield")
    )


@app.route("/download/<token>")
def download(token: str):
    data = RESULTS_STORE.get(token)
    if not data:
        flash("Your download link has expired. Please re-run the analysis.", "warning")
        return redirect(url_for("analyze"))
    # One-time download
    RESULTS_STORE.pop(token, None)
    return send_file(
        io.BytesIO(data),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"fraud_predictions.csv"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
