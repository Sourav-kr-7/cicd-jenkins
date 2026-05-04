from __future__ import annotations

import os
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest

# 🔥 Metric: count all incoming requests
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

def create_app() -> Flask:
    app = Flask(__name__)

    @app.before_request
    def before_request():
        # Increment metric for every request
        REQUEST_COUNT.labels(method="GET", endpoint="all").inc()

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/")
    def root():
        return jsonify(
            message="CI/CD Automation Project",
            env=os.getenv("APP_ENV", "local")
        )

    # 🔥 Prometheus endpoint
    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
