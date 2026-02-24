"""
Purview Policy Simulator - Flask Application
"""

import os

from flask import Flask, jsonify, render_template, request

from simulator import simulate

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/simulate", methods=["POST"])
def run_simulation():
    data = request.get_json(silent=True) or {}
    user_input = str(data.get("requirement", "")).strip()

    if not user_input:
        return jsonify({"error": "Please provide a policy requirement description."}), 400

    result = simulate(user_input)
    return jsonify(result)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=5000)
