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

    SCENE_ENTITY_IDS = {
        "home_2077_city": os.getenv('SCENE_HOME_2077_CITY', os.getenv('SCENE_MAINFRAME_BREACH', 'scene.home_2077_city')),
        "bladerunner_orange": os.getenv('SCENE_BLADERUNNER_ORANGE', 'scene.home_bladerunner_orange'),
        "energize": os.getenv('SCENE_ENERGIZE', 'scene.home_energize'),
        "club": os.getenv('SCENE_CLUB', os.getenv('SCENE_PARTY_MODE', 'scene.home_club')),
        "matrix": os.getenv('SCENE_MATRIX', os.getenv('SCENE_MATRIX_GREEN', 'scene.home_matrix')),
        "nostromo_alarm": os.getenv('SCENE_NOSTROMO_ALARM', os.getenv('SCENE_RED_ALERT', 'scene.home_nostromo_alarm')),
        "relax": os.getenv('SCENE_RELAX', os.getenv('SCENE_NORMAL', 'scene.home_relax')),
    }
    SCENE_SPOTIFY_URIS = {
        "home_2077_city": os.getenv('SCENE_HOME_2077_CITY_SPOTIFY_URI', ''),
        "bladerunner_orange": os.getenv('SCENE_BLADERUNNER_ORANGE_SPOTIFY_URI', ''),
        "energize": os.getenv('SCENE_ENERGIZE_SPOTIFY_URI', ''),
        "club": os.getenv('SCENE_CLUB_SPOTIFY_URI', ''),
        "matrix": os.getenv('SCENE_MATRIX_SPOTIFY_URI', ''),
        "nostromo_alarm": os.getenv('SCENE_NOSTROMO_ALARM_SPOTIFY_URI', ''),
        "relax": os.getenv('SCENE_RELAX_SPOTIFY_URI', ''),
    }
    HUE_DYNAMIC_SCENES = _bool_env('HUE_DYNAMIC_SCENES', True)
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
