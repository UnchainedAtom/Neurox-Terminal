"""
Configuration module for Neurox Terminal.
Loads configuration from environment variables and .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _csv_env(name):
    return [
        value.strip()
        for value in os.getenv(name, '').split(',')
        if value.strip()
    ]


def _bool_env(name, default=False):
    value = os.getenv(name, str(default)).lower()
    return value in ('true', '1', 't', 'yes', 'y')


def _optional_int_env(name):
    value = os.getenv(name, '').strip()
    return int(value) if value else None


def _optional_float_env(name):
    value = os.getenv(name, '').strip()
    return float(value) if value else None


def _room_env_key(room_key, suffix):
    return f"ROOM_{room_key.upper()}_{suffix}"


def _room_label(room_key):
    return room_key.replace("_", " ").title()


DEFAULT_ROOM_ORDER = [
    "dnd_room",
    "living_room",
    "kitchen",
    "entryway",
    "backyard",
    "all_lights",
]

DEFAULT_ROOM_ENTITIES = {
    "dnd_room": ["light.dnd_room", "light.art_display"],
    "living_room": ["light.living_room_lamp", "light.living_room_station_lamp"],
    "kitchen": ["light.kitchen_table"],
    "entryway": ["light.entryway", "light.laundry_room_entryway"],
    "backyard": [
        "switch.tp_link_smart_plug_d528_lights1",
        "switch.tp_link_smart_plug_d528_lights2",
    ],
}

DEFAULT_ROOM_LABELS = {
    "dnd_room": "DND Room",
    "living_room": "Living Room",
    "kitchen": "Kitchen",
    "entryway": "Entryway",
    "backyard": "Backyard Lights",
    "all_lights": "All Lights",
}


class Config:
    """Application configuration."""

    # Home Assistant settings, default to localhost for testing in demo mode
    HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL', 'http://localhost:8123')
    HOME_ASSISTANT_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN', '')

    # Dashboard defaults
    DEFAULT_ROOM = os.getenv('DEFAULT_ROOM', 'home')
    DEFAULT_DASHBOARD_MODE = os.getenv('DEFAULT_DASHBOARD_MODE', 'lighting')

    # Entity configuration
    LIGHT_ENTITY_ID = os.getenv('LIGHT_ENTITY_ID', 'light.overhead_light')
    LIGHT_ENTITY_IDS = _csv_env('LIGHT_ENTITY_IDS')
    BACKYARD_LIGHT_ENTITY_IDS = _csv_env('BACKYARD_LIGHT_ENTITY_IDS')
    ROOM_ORDER = _csv_env('ROOM_ORDER') or DEFAULT_ROOM_ORDER

    SCENE_ENTITY_IDS = {
        "home_2077_city": os.getenv('SCENE_HOME_2077_CITY', os.getenv('SCENE_MAINFRAME_BREACH', 'scene.home_2077_city')),
        "bladerunner_orange": os.getenv('SCENE_BLADERUNNER_ORANGE', 'scene.home_bladerunner_orange'),
        "energize": os.getenv('SCENE_ENERGIZE', 'scene.home_energize'),
        "club": os.getenv('SCENE_CLUB', os.getenv('SCENE_PARTY_MODE', 'scene.home_club')),
        "matrix": os.getenv('SCENE_MATRIX', os.getenv('SCENE_MATRIX_GREEN', 'scene.home_matrix')),
        "nostromo_alarm": os.getenv('SCENE_NOSTROMO_ALARM', os.getenv('SCENE_RED_ALERT', 'scene.home_nostromo_alarm')),
        "blackout": os.getenv('SCENE_BLACKOUT', 'scene.blackout'),
        "relax": os.getenv('SCENE_RELAX', os.getenv('SCENE_NORMAL', 'scene.home_relax')),
    }
    SCENE_SPOTIFY_URIS = {
        "home_2077_city": os.getenv('SCENE_HOME_2077_CITY_SPOTIFY_URI', ''),
        "bladerunner_orange": os.getenv('SCENE_BLADERUNNER_ORANGE_SPOTIFY_URI', ''),
        "energize": os.getenv('SCENE_ENERGIZE_SPOTIFY_URI', ''),
        "club": os.getenv('SCENE_CLUB_SPOTIFY_URI', ''),
        "matrix": os.getenv('SCENE_MATRIX_SPOTIFY_URI', ''),
        "nostromo_alarm": os.getenv('SCENE_NOSTROMO_ALARM_SPOTIFY_URI', ''),
        "blackout": os.getenv('SCENE_BLACKOUT_SPOTIFY_URI', ''),
        "relax": os.getenv('SCENE_RELAX_SPOTIFY_URI', ''),
    }
    HUE_DYNAMIC_SCENES = _bool_env('HUE_DYNAMIC_SCENES', True)
    HUE_DYNAMIC_SCENE_KEYS = _csv_env('HUE_DYNAMIC_SCENE_KEYS') or [
        "home_2077_city",
        "bladerunner_orange",
        "energize",
        "club",
        "matrix",
        "nostromo_alarm",
        "relax",
    ]
    HUE_SCENE_BRIGHTNESS = _optional_int_env('HUE_SCENE_BRIGHTNESS')
    HUE_SCENE_SPEED = _optional_float_env('HUE_SCENE_SPEED')
    HUE_SCENE_TRANSITION = _optional_int_env('HUE_SCENE_TRANSITION')

    # Media settings, default to a sample media file path for demo mode
    MEDIA_PATH = os.getenv('MEDIA_PATH', '/home/pi/media.mp4')
    MEDIA_PLAYER_ENTITY_IDS = _csv_env('MEDIA_PLAYER_ENTITY_IDS')
    SPOTIFY_MEDIA_PLAYER_ENTITY_ID = os.getenv('SPOTIFY_MEDIA_PLAYER_ENTITY_ID', 'media_player.spotify')
    PLEX_MEDIA_PLAYER_ENTITY_ID = os.getenv('PLEX_MEDIA_PLAYER_ENTITY_ID', '')
    SPOTIFY_DEFAULT_SOURCE = os.getenv('SPOTIFY_DEFAULT_SOURCE', '')
    SPOTIFY_PARTY_PLAYLIST_URI = os.getenv('SPOTIFY_PARTY_PLAYLIST_URI', '')
    SPOTIFY_AMBIENT_PLAYLIST_URI = os.getenv('SPOTIFY_AMBIENT_PLAYLIST_URI', '')

    # CRT burn-in protection
    SCREENSAVER_ENABLED = _bool_env('SCREENSAVER_ENABLED', True)
    SCREENSAVER_TIMEOUT_SECONDS = int(os.getenv('SCREENSAVER_TIMEOUT_SECONDS', 300))
    SCREENSAVER_MODES = _csv_env('SCREENSAVER_MODES') or [
        "drifting_diagnostics",
        "matrix_rain",
        "brain_drift",
    ]
    SCREENSAVER_IMAGE_PATHS = _csv_env('SCREENSAVER_IMAGE_PATHS')

    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 8000))

    # Demo mode (when True, doesn't require Home Assistant connection)
    DEMO_MODE = _bool_env('DEMO_MODE', False)

    @classmethod
    def validate(cls):
        """Validate configuration. Raises error if required settings are invalid."""
        if not cls.DEMO_MODE and not cls.HOME_ASSISTANT_TOKEN:
            raise ValueError(
                "HOME_ASSISTANT_TOKEN is required. "
                "Set it in .env file or environment variables, "
                "or enable DEMO_MODE=True for testing."
            )

    @classmethod
    def room_groups(cls):
        """Return room groups configured from environment variables."""
        rooms = {}
        for room_key in cls.ROOM_ORDER:
            if room_key == "all_lights":
                default_entities = cls.LIGHT_ENTITY_IDS
                default_label = "All Lights"
            elif room_key == "backyard":
                default_entities = (
                    cls.BACKYARD_LIGHT_ENTITY_IDS
                    or DEFAULT_ROOM_ENTITIES.get(room_key, [])
                )
                default_label = "Backyard Lights"
            else:
                default_entities = DEFAULT_ROOM_ENTITIES.get(room_key, [])
                default_label = DEFAULT_ROOM_LABELS.get(room_key, _room_label(room_key))

            label = os.getenv(_room_env_key(room_key, "LABEL"), default_label)
            entities = _csv_env(_room_env_key(room_key, "ENTITIES")) or default_entities
            if entities:
                rooms[room_key] = {
                    "key": room_key,
                    "label": label,
                    "entity_ids": entities,
                }
        return rooms

    @classmethod
    def screensaver_public_config(cls):
        """Return frontend-safe screensaver configuration."""
        return {
            "enabled": cls.SCREENSAVER_ENABLED,
            "timeoutSeconds": cls.SCREENSAVER_TIMEOUT_SECONDS,
            "modes": cls.SCREENSAVER_MODES,
            "imagePaths": cls.SCREENSAVER_IMAGE_PATHS,
        }
