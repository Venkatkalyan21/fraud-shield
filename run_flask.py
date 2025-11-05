#!/usr/bin/env python3
"""
Helper launcher for the Flask app.
Runs the Flask development server on http://localhost:5000
"""
from flask_app import app

if __name__ == "__main__":
    # You can change port here if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
