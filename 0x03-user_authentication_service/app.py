#!/usr/bin/env python3
"""
A basic flask app
"""
from flask import Flask, jsonify

app = Flask(__name__)


def message():
    """
    A function that prints a basic message
    """

    return jsonify({"message": "Bienvenue"})


@app.get('/')(message)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
