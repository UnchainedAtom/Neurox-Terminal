"""
Configuration module for Neurox Terminal.
Loads configuration from environment variables and .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Home Assistant settings
    HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL', 'http://localhost:8123')
    HOME_ASSISTANT_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN', '')
    
    # Entity configuration
    LIGHT_ENTITY_ID = os.getenv('LIGHT_ENTITY_ID', 'light.overhead_light')
    
    # Media settings
    MEDIA_PATH = os.getenv('MEDIA_PATH', '/home/pi/media.mp4')
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Demo mode (when True, doesn't require Home Assistant connection)
    DEMO_MODE = os.getenv('DEMO_MODE', 'False').lower() in ('true', '1', 't')
    
    @classmethod
    def validate(cls):
        """Validate configuration. Raises error if required settings are invalid."""
        if not cls.DEMO_MODE and not cls.HOME_ASSISTANT_TOKEN:
            raise ValueError(
                "HOME_ASSISTANT_TOKEN is required. "
                "Set it in .env file or environment variables, "
                "or enable DEMO_MODE=True for testing."
            )
