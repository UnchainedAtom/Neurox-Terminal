"""
Controller module for managing smart device interactions via Home Assistant.
Supports demo mode for testing without Home Assistant connection.
"""
import os
import logging
import requests
from app.config import Config

logger = logging.getLogger(__name__)


def _get_headers():
    """Build authorization headers for Home Assistant API."""
    return {
        "Authorization": f"Bearer {Config.HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json",
    }


def toggle_lights():
    """
    Toggle the configured light entity.
    
    Returns:
        dict: Response with status and details
    """
    if Config.DEMO_MODE:
        logger.info("DEMO MODE: Lights toggled (virtual)")
        return {"status": "success", "demo": True, "message": "Lights toggled (demo mode)"}
    
    try:
        url = f"{Config.HOME_ASSISTANT_URL}/api/services/light/toggle"
        payload = {"entity_id": Config.LIGHT_ENTITY_ID}
        headers = _get_headers()
        
        logger.info(f"Toggling light: {Config.LIGHT_ENTITY_ID}")
        response = requests.post(
            url, 
            json=payload, 
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            logger.info("Light toggled successfully")
            return {"status": "success", "response": response.json()}
        else:
            error_msg = f"Home Assistant error: {response.status_code}"
            logger.error(f"Failed to toggle light: {error_msg}")
            return {"status": "error", "details": response.text}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to connect to Home Assistant: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "details": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error toggling lights: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "details": error_msg}


def play_media(media_path=None):
    """
    Play media file using vlc.
    
    Args:
        media_path (str, optional): Path to media file. Uses config if not provided.
        
    Returns:
        dict: Response with status
    """
    if Config.DEMO_MODE:
        logger.info(f"DEMO MODE: Playing media (virtual)")
        return {"status": "success", "demo": True, "message": "Media playing (demo mode)"}
    
    try:
        path = media_path or Config.MEDIA_PATH
        
        if not os.path.exists(path):
            error_msg = f"Media file not found: {path}"
            logger.warning(error_msg)
            return {"status": "error", "details": error_msg}
        
        logger.info(f"Starting media playback: {path}")
        os.system(f"vlc {path} &")
        return {"status": "success", "message": "media playing"}
        
    except Exception as e:
        error_msg = f"Error playing media: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "details": error_msg}