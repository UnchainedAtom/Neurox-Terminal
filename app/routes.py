"""
Routes module for Neurox Terminal API.
Defines all HTTP endpoints for device control.
"""
import logging
from flask import Flask, jsonify, render_template
from app.config import Config
from app.controller import toggle_lights, play_media

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Validate configuration on startup
try:
    Config.validate()
except ValueError as e:
    logger.warning(f"Configuration warning: {e}")


@app.route("/")
def index():
    """Serve the main dashboard UI."""
    return render_template('dashboard.html')


@app.route("/api/")
def api_index():
    """Health check endpoint."""
    demo_mode = " (DEMO MODE)" if Config.DEMO_MODE else ""
    return jsonify({
        "status": "running",
        "service": "Neurox Terminal API",
        "demo_mode": Config.DEMO_MODE,
        "message": f"Neuroxnode API is running{demo_mode}"
    }), 200


@app.route("/api/status")
def api_status():
    """Return detailed service status."""
    return jsonify({
        "status": "operational",
        "demo_mode": Config.DEMO_MODE,
        "home_assistant_configured": bool(Config.HOME_ASSISTANT_TOKEN),
        "endpoints": [
            "/api/toggle-lights",
            "/api/play-media",
            "/api/status"
        ]
    }), 200

# TODO: Add more endpoints for additional device controls (e.g., thermostat, security system)
@app.route("/api/toggle-lights", methods=["POST"])
def api_toggle_lights():
    """
    Toggle the configured light entity.
    
    Returns:
        JSON response with status
    """
    logger.info("Light toggle request received")
    try:
        result = toggle_lights()
        
        if result.get("status") == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in toggle lights endpoint: {e}")
        return jsonify({"status": "error", "details": str(e)}), 500

# TODO: Add endpoint for playing media files via VLC or similar media player
# TODO: Need to figure out architecture for media playback still
@app.route("/api/play-media", methods=["POST"])
def api_play_media():
    """
    Play media file via VLC.
    
    Returns:
        JSON response with status
    """
    logger.info("Media play request received")
    try:
        result = play_media()
        
        if result.get("status") == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in play media endpoint: {e}")
        return jsonify({"status": "error", "details": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {error}")
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
