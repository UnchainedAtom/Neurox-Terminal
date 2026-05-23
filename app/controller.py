"""
Controller module for managing smart device interactions via Home Assistant.
Supports demo mode for testing without Home Assistant connection.
"""
import os
import logging
from app.config import Config
from app.home_assistant import get_states, turn_off_light, turn_on_light, turn_on_scene, call_service

logger = logging.getLogger(__name__)

SCENE_LABELS = {
    "party_mode": "Party Mode",
    "matrix_green": "Matrix Green",
    "red_alert": "Red Alert",
    "blackout": "Blackout",
    "normal": "Normal",
    "mainframe_breach": "Mainframe Breach",
}


def _demo_lighting_dashboard():
    """Return safe demo data for local development without Home Assistant."""
    return {
        "status": "success",
        "demo": True,
        "home_assistant_available": False,
        "message": "Demo mode active. Home Assistant calls are simulated.",
        "default_room": Config.DEFAULT_ROOM,
        "default_dashboard_mode": Config.DEFAULT_DASHBOARD_MODE,
        "lights": [
            {
                "entity_id": Config.LIGHT_ENTITY_ID,
                "name": "Overhead Light",
                "state": "off",
                "area": Config.DEFAULT_ROOM,
            },
            {
                "entity_id": "light.terminal_backlight",
                "name": "Terminal Backlight",
                "state": "on",
                "area": Config.DEFAULT_ROOM,
            },
        ],
        "scenes": _configured_scenes(),
    }


def _configured_scenes():
    return [
        {
            "key": key,
            "label": SCENE_LABELS.get(key, key.replace("_", " ").title()),
            "entity_id": entity_id,
        }
        for key, entity_id in Config.SCENE_ENTITY_IDS.items()
        if entity_id
    ]


def _friendly_name(state):
    return state.get("attributes", {}).get("friendly_name") or state.get("entity_id")


def _filter_entities(states, domain):
    entities = [
        {
            "entity_id": item.get("entity_id"),
            "name": _friendly_name(item),
            "state": item.get("state", "unknown"),
            "area": item.get("attributes", {}).get("area_id", ""),
        }
        for item in states
        if item.get("entity_id", "").startswith(f"{domain}.")
    ]

    if domain == "light" and Config.LIGHT_ENTITY_IDS:
        allowed = set(Config.LIGHT_ENTITY_IDS)
        entities = [entity for entity in entities if entity["entity_id"] in allowed]

    return sorted(entities, key=lambda entity: entity["name"].lower())


def get_lighting_dashboard():
    """Return lighting data for the dashboard."""
    if Config.DEMO_MODE:
        return _demo_lighting_dashboard()

    states_result = get_states()
    if states_result.get("status") != "success":
        return {
            "status": "error",
            "demo": False,
            "home_assistant_available": False,
            "message": states_result.get("message", "Home Assistant unavailable."),
            "default_room": Config.DEFAULT_ROOM,
            "default_dashboard_mode": Config.DEFAULT_DASHBOARD_MODE,
            "lights": [],
            "scenes": _configured_scenes(),
        }

    states = states_result.get("data", [])
    return {
        "status": "success",
        "demo": False,
        "home_assistant_available": True,
        "default_room": Config.DEFAULT_ROOM,
        "default_dashboard_mode": Config.DEFAULT_DASHBOARD_MODE,
        "lights": _filter_entities(states, "light"),
        "scenes": _configured_scenes(),
    }


def set_light(entity_id, action):
    """Turn a light entity on or off."""
    if action not in ("turn-on", "turn-off"):
        return {"status": "error", "message": "Unsupported light action."}

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: %s %s", action, entity_id)
        return {
            "status": "success",
            "demo": True,
            "message": f"{entity_id} {action.replace('-', ' ')} simulated.",
        }

    service = turn_on_light if action == "turn-on" else turn_off_light
    result = service(entity_id)
    if result.get("status") == "success":
        result["message"] = f"{entity_id} {action.replace('-', ' ')} sent."
    return result


def run_scene(scene_key):
    """Activate a configured scene by key."""
    entity_id = Config.SCENE_ENTITY_IDS.get(scene_key)
    if not entity_id:
        return {"status": "error", "message": f"Unknown scene key: {scene_key}"}

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: scene %s activated as %s", scene_key, entity_id)
        return {
            "status": "success",
            "demo": True,
            "message": f"{SCENE_LABELS.get(scene_key, scene_key)} simulated.",
            "entity_id": entity_id,
        }

    result = turn_on_scene(entity_id)
    if result.get("status") == "success":
        result["message"] = f"{SCENE_LABELS.get(scene_key, scene_key)} activated."
        result["entity_id"] = entity_id
    return result


def toggle_lights():
    """
    Toggle the configured light entity.
    
    Returns:
        dict: Response with status and details
    """
    if Config.DEMO_MODE:
        logger.info("DEMO MODE: Lights toggled (virtual)")
        return {"status": "success", "demo": True, "message": "Lights toggled (demo mode)"}

    result = call_service("light", "toggle", {"entity_id": Config.LIGHT_ENTITY_ID})
    if result.get("status") == "success":
        result["message"] = "Light toggle sent."
    return result


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
