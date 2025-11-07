import os
import json
from flask import Flask, request, jsonify

from services.incident_service import create_service

CONFIG_PATH = "config.json"

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Configuration file {CONFIG_PATH} not found!")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DB_PATH = config["database"]["path"]
HOST = config["service"]["host"]
PORT = config["service"]["port"]
DEBUG = config["service"]["debug"]

app = create_service(DB_PATH)

if __name__ == '__main__':
    app.run(HOST, PORT, DEBUG)