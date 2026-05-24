"""
Controller module for managing smart device interactions via Home Assistant.
Supports demo mode for testing without Home Assistant connection.
"""
import os
import logging
from app.config import Config
from app.home_assistant import activate_hue_scene, get_states, turn_on_scene, call_service

logger = logging.getLogger(__name__)

SCENE_LABELS = {
    "home_2077_city": "2077 City",
    "bladerunner_orange": "Bladerunner Orange",
    "energize": "Clear the Club",
    "club": "Club",
    "matrix": "Matrix",
    "nostromo_alarm": "Nostromo Alarm",
    "blackout": "Blackout",
    "relax": "Relax",
}

MEDIA_ACTIONS = {
    "play-pause": "media_play_pause",
    "next": "media_next_track",
    "previous": "media_previous_track",
    "stop": "media_stop",
}

DEMO_LIGHT_ENTITY_IDS = [
    "light.art_display",
    "light.dnd_room",
    "light.entryway",
    "light.kitchen_table",
    "light.laundry_room_entryway",
    "light.living_room_lamp",
    "light.living_room_station_lamp",
    "switch.tp_link_smart_plug_d528_lights1",
    "switch.tp_link_smart_plug_d528_lights2",
]

DEMO_BACKYARD_LIGHT_ENTITY_IDS = [
    "switch.tp_link_smart_plug_d528_lights1",
    "switch.tp_link_smart_plug_d528_lights2",
]


def _name_from_entity_id(entity_id):
    return entity_id.split(".", 1)[-1].replace("_", " ").title()


def _demo_control_entity(entity_id, state="off"):
    domain = entity_id.split(".", 1)[0] if "." in entity_id else ""
    return {
        "entity_id": entity_id,
        "name": _name_from_entity_id(entity_id),
        "state": state,
        "area": "backyard" if entity_id in DEMO_BACKYARD_LIGHT_ENTITY_IDS else Config.DEFAULT_ROOM,
        "domain": domain,
    }


def _demo_lighting_dashboard():
    """Return safe demo data for local development without Home Assistant."""
    light_ids = Config.LIGHT_ENTITY_IDS or DEMO_LIGHT_ENTITY_IDS
    backyard_ids = Config.BACKYARD_LIGHT_ENTITY_IDS or DEMO_BACKYARD_LIGHT_ENTITY_IDS

    return {
        "status": "success",
        "demo": True,
        "home_assistant_available": False,
        "message": "Demo mode active. Home Assistant calls are simulated.",
        "default_room": Config.DEFAULT_ROOM,
        "default_dashboard_mode": Config.DEFAULT_DASHBOARD_MODE,
        "lights": [_demo_control_entity(entity_id) for entity_id in light_ids],
        "backyard_lights": [_demo_control_entity(entity_id) for entity_id in backyard_ids],
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


def _entity_summary(item):
    entity_id = item.get("entity_id", "")
    domain = entity_id.split(".", 1)[0] if "." in entity_id else ""
    return {
        "entity_id": entity_id,
        "name": _friendly_name(item),
        "state": item.get("state", "unknown"),
        "area": item.get("attributes", {}).get("area_id", ""),
        "domain": domain,
    }


def _filter_control_entities(states, entity_ids=None):
    allowed = set(entity_ids or [])
    entities = []
    for item in states:
        entity_id = item.get("entity_id", "")
        domain = entity_id.split(".", 1)[0] if "." in entity_id else ""
        if domain not in ("light", "switch"):
            continue
        if allowed and entity_id not in allowed:
            continue
        entities.append(_entity_summary(item))

    return sorted(entities, key=lambda entity: entity["name"].lower())


def _filter_media_players(states):
    players = []
    for item in states:
        entity_id = item.get("entity_id", "")
        if not entity_id.startswith("media_player."):
            continue

        attributes = item.get("attributes", {})
        players.append({
            "entity_id": entity_id,
            "name": _friendly_name(item),
            "state": item.get("state", "unknown"),
            "source": attributes.get("source", ""),
            "source_list": attributes.get("source_list", []),
            "media_title": attributes.get("media_title", ""),
            "media_artist": attributes.get("media_artist", ""),
        })

    if Config.MEDIA_PLAYER_ENTITY_IDS:
        allowed = set(Config.MEDIA_PLAYER_ENTITY_IDS)
        players = [player for player in players if player["entity_id"] in allowed]

    return sorted(players, key=lambda player: player["name"].lower())


def _media_presets():
    presets = []
    if Config.SPOTIFY_PARTY_PLAYLIST_URI:
        presets.append({
            "key": "spotify_party",
            "label": "Spotify Party Playlist",
            "entity_id": Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID,
        })
    if Config.SPOTIFY_AMBIENT_PLAYLIST_URI:
        presets.append({
            "key": "spotify_ambient",
            "label": "Spotify Ambient Playlist",
            "entity_id": Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID,
        })
    if Config.SPOTIFY_DEFAULT_SOURCE:
        presets.append({
            "key": "spotify_source",
            "label": "Select Spotify Source",
            "entity_id": Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID,
        })
    return presets


def _demo_media_dashboard():
    return {
        "status": "success",
        "demo": True,
        "home_assistant_available": False,
        "message": "Demo mode active. Media calls are simulated.",
        "media_players": [
            {
                "entity_id": Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID,
                "name": "Spotify",
                "state": "idle",
                "source": Config.SPOTIFY_DEFAULT_SOURCE or "Demo Speaker",
                "source_list": [Config.SPOTIFY_DEFAULT_SOURCE or "Demo Speaker"],
                "media_title": "No active track",
                "media_artist": "",
            },
            {
                "entity_id": Config.PLEX_MEDIA_PLAYER_ENTITY_ID or "media_player.plex_demo",
                "name": "Plex Relay",
                "state": "idle",
                "source": "",
                "source_list": [],
                "media_title": "Plex client standby",
                "media_artist": "",
            },
        ],
        "presets": _media_presets(),
    }


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
            "backyard_lights": [],
            "scenes": _configured_scenes(),
        }

    states = states_result.get("data", [])
    return {
        "status": "success",
        "demo": False,
        "home_assistant_available": True,
        "default_room": Config.DEFAULT_ROOM,
        "default_dashboard_mode": Config.DEFAULT_DASHBOARD_MODE,
        "lights": _filter_control_entities(states, Config.LIGHT_ENTITY_IDS),
        "backyard_lights": _filter_control_entities(states, Config.BACKYARD_LIGHT_ENTITY_IDS),
        "scenes": _configured_scenes(),
    }


def get_media_dashboard():
    """Return Home Assistant media player state for the dashboard."""
    if Config.DEMO_MODE:
        return _demo_media_dashboard()

    states_result = get_states()
    if states_result.get("status") != "success":
        return {
            "status": "error",
            "demo": False,
            "home_assistant_available": False,
            "message": states_result.get("message", "Home Assistant unavailable."),
            "media_players": [],
            "presets": _media_presets(),
        }

    return {
        "status": "success",
        "demo": False,
        "home_assistant_available": True,
        "media_players": _filter_media_players(states_result.get("data", [])),
        "presets": _media_presets(),
    }


def set_light(entity_id, action):
    """Turn a light or switch entity on or off."""
    if action not in ("turn-on", "turn-off"):
        return {"status": "error", "message": "Unsupported light action."}

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: %s %s", action, entity_id)
        return {
            "status": "success",
            "demo": True,
            "message": f"{entity_id} {action.replace('-', ' ')} simulated.",
        }

    domain = entity_id.split(".", 1)[0] if "." in entity_id else "light"
    if domain not in ("light", "switch"):
        return {"status": "error", "message": f"Unsupported lighting domain: {domain}"}

    service = "turn_on" if action == "turn-on" else "turn_off"
    result = call_service(domain, service, {"entity_id": entity_id})
    if result.get("status") == "success":
        result["message"] = f"{entity_id} {action.replace('-', ' ')} sent."
    return result


def run_scene(scene_key):
    """Activate a configured scene by key."""
    entity_id = Config.SCENE_ENTITY_IDS.get(scene_key)
    if not entity_id:
        return {"status": "error", "message": f"Unknown scene key: {scene_key}"}

    spotify_uri = Config.SCENE_SPOTIFY_URIS.get(scene_key, "")

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: scene %s activated as %s", scene_key, entity_id)
        return {
            "status": "success",
            "demo": True,
            "message": _scene_message(scene_key, bool(spotify_uri), demo=True),
            "entity_id": entity_id,
            "spotify_uri_configured": bool(spotify_uri),
        }

    result = activate_hue_scene(entity_id) if Config.HUE_DYNAMIC_SCENES else turn_on_scene(entity_id)
    if result.get("status") != "success":
        return result

    spotify_result = _run_scene_spotify(spotify_uri)
    result["message"] = _scene_message(scene_key, spotify_result.get("status") == "success")
    result["entity_id"] = entity_id
    result["spotify"] = spotify_result
    return result


def _scene_message(scene_key, spotify_started=False, demo=False):
    label = SCENE_LABELS.get(scene_key, scene_key)
    suffix = " simulated" if demo else " activated"
    if spotify_started:
        suffix += " with Spotify playlist"
    return f"{label}{suffix}."


def _run_scene_spotify(spotify_uri):
    """Start a Spotify playlist for a scene when configured."""
    if not spotify_uri:
        return {"status": "skipped", "message": "No Spotify playlist configured for this scene."}

    if Config.SPOTIFY_DEFAULT_SOURCE:
        source_result = select_media_source(Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID, Config.SPOTIFY_DEFAULT_SOURCE)
        if source_result.get("status") != "success":
            return source_result

    result = call_service(
        "media_player",
        "play_media",
        {
            "entity_id": Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID,
            "media_content_id": spotify_uri,
            "media_content_type": "playlist",
        },
    )
    if result.get("status") == "success":
        result["message"] = "Scene Spotify playlist started."
    return result


def set_media_action(entity_id, action):
    """Run a standard Home Assistant media_player action."""
    service = MEDIA_ACTIONS.get(action)
    if not service:
        return {"status": "error", "message": "Unsupported media action."}

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: media %s %s", action, entity_id)
        return {
            "status": "success",
            "demo": True,
            "message": f"{entity_id} {action.replace('-', ' ')} simulated.",
        }

    result = call_service("media_player", service, {"entity_id": entity_id})
    if result.get("status") == "success":
        result["message"] = f"{entity_id} {action.replace('-', ' ')} sent."
    return result


def select_media_source(entity_id, source):
    """Select a media_player source."""
    if not source:
        return {"status": "error", "message": "Media source is required."}

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: source %s selected for %s", source, entity_id)
        return {"status": "success", "demo": True, "message": f"{source} selected."}

    result = call_service("media_player", "select_source", {"entity_id": entity_id, "source": source})
    if result.get("status") == "success":
        result["message"] = f"{source} selected."
    return result


def run_media_preset(preset_key):
    """Run a configured media preset."""
    if preset_key == "spotify_source":
        return select_media_source(Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID, Config.SPOTIFY_DEFAULT_SOURCE)

    playlist_uri = {
        "spotify_party": Config.SPOTIFY_PARTY_PLAYLIST_URI,
        "spotify_ambient": Config.SPOTIFY_AMBIENT_PLAYLIST_URI,
    }.get(preset_key)

    if not playlist_uri:
        return {"status": "error", "message": f"Unknown media preset: {preset_key}"}

    if Config.DEMO_MODE:
        logger.info("DEMO MODE: media preset %s", preset_key)
        return {"status": "success", "demo": True, "message": f"{preset_key.replace('_', ' ')} simulated."}

    result = call_service(
        "media_player",
        "play_media",
        {
            "entity_id": Config.SPOTIFY_MEDIA_PLAYER_ENTITY_ID,
            "media_content_id": playlist_uri,
            "media_content_type": "playlist",
        },
    )
    if result.get("status") == "success":
        result["message"] = f"{preset_key.replace('_', ' ').title()} started."
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
