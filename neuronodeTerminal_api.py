"""
Neurox Terminal API - Home automation terminal control system
A Flask-based API for controlling smart devices via Home Assistant
"""
import logging
from app.config import Config
from app.routes import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting Neurox Terminal API")
    logger.info(f"Demo Mode: {Config.DEMO_MODE}")
    logger.info(f"Listening on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )