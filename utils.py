"""
Utility functions for the Fraud Detection System
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Tuple, Optional, Dict, Any
import streamlit as st

def validate_csv_data(data: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that the uploaded CSV contains the expected structure
    
    Args:
        data: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if we have enough columns
    if len(data.columns) < 5:
        return False, "CSV must contain at least 5 columns"
    
    # Check for expected feature columns (V1, V2, V3, etc.)
    expected_features = [f"V{i}" for i in range(1, 29)]
    missing_features = [col for col in expected_features if col not in data.columns]
    
    if len(missing_features) > 20:  # Allow some flexibility
        return False, f"Missing many expected feature columns: {missing_features[:5]}..."
    
    # Check data types - should be numeric
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) < len(data.columns) * 0.8:
        return False, "Most columns should be numeric"
    
    return True, "Data validation passed"

def prepare_data_for_prediction(data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
    """
    Prepare data for model prediction
    
    Args:
        data: Raw DataFrame
        
    Returns:
        Tuple of (features_df, actual_labels)
    """
    # Check if 'Class' column exists (for evaluation)
    actual_labels = None
    if 'Class' in data.columns:
        actual_labels = data['Class']
        features_df = data.drop('Class', axis=1)
    else:
        features_df = data
    
    # Ensure all columns are numeric
    for col in features_df.columns:
        if not pd.api.types.is_numeric_dtype(features_df[col]):
            try:
                features_df[col] = pd.to_numeric(features_df[col], errors='coerce')
            except:
                features_df[col] = 0
    
    # Fill any NaN values with 0
    features_df = features_df.fillna(0)
    
    return features_df, actual_labels

def calculate_risk_metrics(predictions: np.ndarray, probabilities: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """
    Calculate risk metrics from predictions
    
    Args:
        predictions: Array of binary predictions (0/1)
        probabilities: Array of fraud probabilities
        
    Returns:
        Dictionary of risk metrics
    """
    total_transactions = len(predictions)
    fraud_count = np.sum(predictions == 1)
    legitimate_count = np.sum(predictions == 0)
    fraud_rate = (fraud_count / total_transactions) * 100
    
    # Determine risk level
    if fraud_rate > 5:
        risk_level = "HIGH"
        risk_icon = "⚠️"
    elif fraud_rate > 2:
        risk_level = "MEDIUM"
        risk_icon = "⚡"
    else:
        risk_level = "LOW"
        risk_icon = "✅"
    
    metrics = {
        "total_transactions": total_transactions,
        "legitimate_count": legitimate_count,
        "fraud_count": fraud_count,
        "fraud_rate": fraud_rate,
        "risk_level": risk_level,
        "risk_icon": risk_icon
    }
    
    if probabilities is not None:
        metrics["avg_fraud_probability"] = np.mean(probabilities)
        metrics["max_fraud_probability"] = np.max(probabilities)
        metrics["min_fraud_probability"] = np.min(probabilities)
    
    return metrics

def create_prediction_visualizations(metrics: Dict[str, Any], probabilities: Optional[np.ndarray] = None) -> Dict[str, go.Figure]:
    """
    Create visualization charts for the predictions
    
    Args:
        metrics: Risk metrics dictionary
        probabilities: Array of fraud probabilities
        
    Returns:
        Dictionary of plotly figures
    """
    figures = {}
    
    # Pie chart for transaction distribution
    fig_pie = px.pie(
        values=[metrics["legitimate_count"], metrics["fraud_count"]],
        names=['Legitimate', 'Fraudulent'],
        title="Transaction Distribution",
        color_discrete_sequence=['#00ff00', '#ff0000']
    )
    fig_pie.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    figures["distribution"] = fig_pie
    
    # Histogram for fraud probabilities if available
    if probabilities is not None:
        fig_hist = px.histogram(
            x=probabilities,
            nbins=20,
            title="Fraud Probability Distribution",
            labels={'x': 'Fraud Probability', 'y': 'Count'},
            color_discrete_sequence=['#667eea']
        )
        fig_hist.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(122, 130, 255, 0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(122, 130, 255, 0.1)')
        )
        figures["probabilities"] = fig_hist
    
    # Bar chart for risk comparison
    fig_bar = go.Figure(data=[
        go.Bar(
            x=['Legitimate', 'Fraudulent'],
            y=[metrics["legitimate_count"], metrics["fraud_count"]],
            marker_color=['#00ff00', '#ff0000']
        )
    ])
    fig_bar.update_layout(
        title="Transaction Counts",
        xaxis_title="Transaction Type",
        yaxis_title="Count",
        autosize=True,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(122, 130, 255, 0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(122, 130, 255, 0.1)')
    )
    figures["counts"] = fig_bar
    
    return figures

def generate_summary_report(metrics: Dict[str, Any], model_path: str) -> str:
    """
    Generate a text summary report
    
    Args:
        metrics: Risk metrics dictionary
        model_path: Path to the model file
        
    Returns:
        Formatted summary report
    """
    report = f"""
Fraud Detection Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
- Total Transactions: {metrics['total_transactions']:,}
- Legitimate Transactions: {metrics['legitimate_count']:,}
- Fraudulent Transactions: {metrics['fraud_count']:,}
- Fraud Rate: {metrics['fraud_rate']:.2f}%
- Risk Level: {metrics['risk_level']} {metrics['risk_icon']}

Model Used: {model_path}

Risk Assessment:
"""
    
    if metrics['risk_level'] == 'HIGH':
        report += "- HIGH RISK: Fraud rate is above 5%. Immediate attention required.\n"
        report += "- Consider implementing additional security measures.\n"
        report += "- Review recent system changes and access patterns.\n"
    elif metrics['risk_level'] == 'MEDIUM':
        report += "- MEDIUM RISK: Fraud rate is between 2-5%. Monitor closely.\n"
        report += "- Review suspicious transactions manually.\n"
        report += "- Consider increasing monitoring frequency.\n"
    else:
        report += "- LOW RISK: Fraud rate is below 2%. Normal operations.\n"
        report += "- Continue with current security protocols.\n"
    
    if 'avg_fraud_probability' in metrics:
        report += f"\nProbability Analysis:\n"
        report += f"- Average Fraud Probability: {metrics['avg_fraud_probability']:.3f}\n"
        report += f"- Maximum Fraud Probability: {metrics['max_fraud_probability']:.3f}\n"
        report += f"- Minimum Fraud Probability: {metrics['min_fraud_probability']:.3f}\n"
    
    return report

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"
