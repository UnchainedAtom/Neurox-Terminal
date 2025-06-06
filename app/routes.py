from flask import Flask, jsonify
from app.controller import toggle_lights, play_media

app = Flask(__name__)

@app.route("/")
def index():
    return "Neuroxnode API is running."

@app.route("/api/toggle-lights")
def api_toggle_lights():
    response = toggle_lights()
    if response.status_code == 200:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "details": response.text}), 500

@app.route("/api/play-media")
def api_play_media():
    result = play_media()
    return jsonify({"status": result})
