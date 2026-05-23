"""Small Home Assistant REST client for Neurox Terminal."""
import logging
from urllib.parse import quote

import requests

from app.config import Config

logger = logging.getLogger(__name__)


def _base_url():
    return Config.HOME_ASSISTANT_URL.rstrip("/")


def _headers():
    return {
        "Authorization": f"Bearer {Config.HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json",
    }


def _unconfigured_result():
    return {
        "status": "error",
        "code": "home_assistant_unconfigured",
        "message": "Home Assistant token is not configured.",
    }


def get_states():
    """Fetch all Home Assistant entity states."""
    if not Config.HOME_ASSISTANT_TOKEN:
        return _unconfigured_result()

    try:
        response = requests.get(
            f"{_base_url()}/api/states",
            headers=_headers(),
            timeout=5,
        )
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as exc:
        logger.error("Home Assistant states request failed: %s", exc)
        return {
            "status": "error",
            "code": "home_assistant_unavailable",
            "message": f"Home Assistant unavailable: {exc}",
        }
    except ValueError as exc:
        logger.error("Home Assistant returned invalid JSON: %s", exc)
        return {
            "status": "error",
            "code": "home_assistant_invalid_response",
            "message": "Home Assistant returned an invalid response.",
        }


def call_service(domain, service, payload):
    """Call a Home Assistant service endpoint."""
    if not Config.HOME_ASSISTANT_TOKEN:
        return _unconfigured_result()

    try:
        safe_domain = quote(domain, safe="")
        safe_service = quote(service, safe="")
        response = requests.post(
            f"{_base_url()}/api/services/{safe_domain}/{safe_service}",
            json=payload,
            headers=_headers(),
            timeout=5,
        )
        response.raise_for_status()
        data = response.json() if response.text else []
        return {"status": "success", "data": data}
    except requests.exceptions.RequestException as exc:
        logger.error("Home Assistant service call failed: %s", exc)
        return {
            "status": "error",
            "code": "home_assistant_service_failed",
            "message": f"Home Assistant service call failed: {exc}",
        }
    except ValueError:
        return {"status": "success", "data": []}


def turn_on_light(entity_id):
    """Turn on a light entity."""
    return call_service("light", "turn_on", {"entity_id": entity_id})


def turn_off_light(entity_id):
    """Turn off a light entity."""
    return call_service("light", "turn_off", {"entity_id": entity_id})


def turn_on_scene(entity_id):
    """Activate a scene entity."""
    return call_service("scene", "turn_on", {"entity_id": entity_id})
