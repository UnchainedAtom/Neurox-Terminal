# Neurox Terminal

A Flask API for controlling smart home devices with a retro terminal style web dashboard and demo mode for testing without Home Assistant.

---

## Overview

**Concept:**  
I have many different smart devices in my house, with many different apps to control them.  I wanted to standardize these items into one location that could be physically interacted with.  I also wanted this to feel like an older retro terminal.  Originally this was developed on a Raspberry Pi, which ran Home Assistant, and connected to an old CRT.  For Demo purposes this only runs locally and mimics the calls that would be made on a real system. 

**Solution:**  
Created a RESTful API backend (Flask + Python) with environment-based configuration, paired with a responsive terminal-themed web UI (HTML/CSS/JavaScript). Includes demo mode for testing without external dependencies, Docker containerization for deployments, and structured logging for operational visibility.

**Outcome:**  
A fully functional smart home control API that works locally (with or without Home Assistant), runs in Docker, and comes with a working web dashboard. Can toggle lights, control media playback, and monitor system status in real-time. Deployable to Raspberry Pi or cloud infrastructure.

---

## Architecture / System Design (High Level)

```
User Browser
    ↓
Web Dashboard (HTML/CSS/JS)
    ↓
REST API Endpoints (Flask Routes)
    ↓
Business Logic (Controller)
    ├→ Demo Mode (mock responses)
    └→ Home Assistant API (if configured)
    ↓
Configuration (Environment Variables)
    ↓
Logging System (structured output)
```

**Flow:**
1. User opens dashboard UI (`GET /`)
2. Frontend fetches status via `GET /api/status`
3. User clicks button (e.g., "Toggle Lights")
4. Frontend posts to `POST /api/toggle-lights`
5. Backend checks demo mode or calls Home Assistant
6. Response returns to frontend, UI updates
7. Activity logged with timestamp

---

## Core Features

- **REST API** - Clean endpoints for device control (`/api/toggle-lights`, `/api/play-media`, `/api/status`)
- **Web Dashboard** - Terminal-style UI with real-time status and activity logging
- **Demo Mode** - Fully functional without Home Assistant (for testing)
- **Environment Configuration** - 12-factor app pattern, no hardcoded secrets
- **Structured Logging** - Timestamped logs for all requests and errors
- **Docker Ready** - Multi-stage Dockerfile with health checks
- **Error Handling** - Proper HTTP status codes and JSON error responses
- **Activity Log** - Real-time event tracking in the UI

---

## Technical Stack

**Languages / Runtime**
- Python 3.11

**Frameworks / Libraries**
- Flask 3.1.1 (API framework)
- Jinja2 3.1.6 (HTML templating)
- python-dotenv 1.0.0 (environment configuration)
- requests 2.32.3 (HTTP client for Home Assistant API)

**Infrastructure / Deployment**
- Docker (containerization)
- Docker Compose (orchestration)

**Frontend**
- HTML5
- CSS3 (custom terminal styling)
- Vanilla JavaScript (API calls, UI updates)

---

## Local Development

### Prerequisites

- Python 3.8+
- pip (package manager)
- Home Assistant (optional - demo mode works without it)
- Docker (optional - for container testing)

### Setup

Clone the repository:

```bash
git clone https://github.com/UnchainedAtom/Neurox-Terminal.git
cd Neurox-Terminal
```

Create virtual environment:

```bash
python3 -m venv neuroxnodeTerminal-venv
source neuroxnodeTerminal-venv/bin/activate  # Windows: neuroxnodeTerminal-venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment:

```bash
cp .env.example .env
```

Edit `.env` file. For demo mode (no Home Assistant needed):

```env
DEMO_MODE=True
FLASK_PORT=8000
```

Or for real Home Assistant integration:

```env
DEMO_MODE=False
HOME_ASSISTANT_URL=http://your-homeassistant:8123
HOME_ASSISTANT_TOKEN=your_long_lived_access_token
LIGHT_ENTITY_ID=light.your_light
FLASK_PORT=8000
```

Run the app:

```bash
python neuronodeTerminal_api.py
```

Default URL: `http://localhost:8000`

---

## Deployment

### With Docker

Build and run:

```bash
docker compose up
```

Runs on `http://localhost:8000` in demo mode.

To use with real Home Assistant, update environment variables in `docker-compose.yml` or pass `.env` file:

```bash
docker compose up --env-file .env
```

### On Raspberry Pi

```bash
./run.sh
```

Creates venv, installs dependencies, and starts the API.

---

## Testing

### Test in Demo Mode

```bash
# Verify .env has DEMO_MODE=True
python neuronodeTerminal_api.py

# In another terminal:

# Health check
curl http://localhost:8000/

# API status
curl http://localhost:8000/api/status

# Toggle lights (returns success in demo)
curl -X POST http://localhost:8000/api/toggle-lights

# Play media (returns success in demo)
curl -X POST http://localhost:8000/api/play-media
```

### Test UI

Open browser: `http://localhost:8000/`

You should see:
- Terminal-style dashboard
- System status panel (API status, demo mode indicator, etc.)
- Control buttons (lights, media)
- Activity log showing each action

### Expected Logs

```
2026-02-26 01:27:33,734 - __main__ - INFO - Starting Neurox Terminal API
2026-02-26 01:27:33,734 - __main__ - INFO - Demo Mode: True
2026-02-26 01:27:33,734 - __main__ - INFO - Listening on 0.0.0.0:8000
```

When you click a button:

```
2026-02-26 18:07:40 - app.routes - INFO - Light toggle request received
2026-02-26 18:07:40 - app.controller - INFO - DEMO MODE: Lights toggled (virtual)
2026-02-26 18:07:40 - werkzeug - INFO - 127.0.0.1 - - [26/Feb/2026 18:07:40] "POST /api/toggle-lights HTTP/1.1" 200
```

---

## Reliability / Operational Considerations

**Error Handling**
- All endpoints return JSON with `status` field
- HTTP status codes are correct (200 success, 404 not found, 500 error)
- Network errors are caught and logged

**Logging Strategy**
- Every request is logged with timestamp
- Error stack traces are printed to console

**Input Validation**
- Configuration validated on startup
- Missing Home Assistant token caught if not in demo mode
- Invalid endpoints return 404 with JSON

**Retry Behavior**
- Current implementation: no automatic retries
- Home Assistant API calls have 5-second timeout
- Failed requests return error response to client

**Health Checks**
- Docker includes HTTP health check endpoint (`/api/status`)
- Checks every 30 seconds
- Container marked unhealthy if endpoint doesn't respond

---

## Known Limitations

- **No database** - Status/history isn't persisted, restarts lose event log
- **Single device** - Currently hardcoded to one light entity and one media path
- **No authentication** - Anyone with network access can control devices
- **Demo mode only mocks responses** - Doesn't actually control real devices
- **Media playback only conept** - Media playback is only conceptual
- **Home Assistant dependency** - Real mode requires Home Assistant instance on same network

---

## Future Improvements

**Feature Additions**
- Support multiple devices (switches, thermostats, sensors)
- Detailed light controls
- Light routine packages 
- User authentication and role-based access control
- Automation/scheduling capabilities
- MQTT support for non-Home Assistant devices
- Database Integration
- Media playback capability
- Media server management

**UI/UX**
- More responsive control types (sliders, color pickers)
- Real-time device state updates via WebSockets
- Optimized layout for varying displays
- More granular details and interaction with devices

**Infrastructure**
- Metrics export
- Structured JSON logging format
- Rate limiting for API endpoints


---

## Notes

**Project Goals:**
This project was built to explore smart home automation and API design while maintaining operational clarity and production practices. It demonstrates configuration management, containerization, error handling, and logging patterns.

**Design Decisions:**
- Demo mode allows complete testing without external dependencies
- Environment variables over config files 
- Docker ensures consistency across environments
- Structured logging makes debugging and monitoring easier
