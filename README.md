# Neurox Terminal

A Flask-based home terminal for a Raspberry Pi / CRT smart-home control panel. Lighting is the primary working module, with Home Assistant as the integration layer and a retro terminal UI built for small-screen readability.

---

## Overview

**Concept:**  
I have many different smart devices in my house, with many different apps to control them. I wanted to standardize these items into one location that could be physically interacted with. The terminal is designed for a Raspberry Pi connected to a PVM CRT, with a readable retro terminal flow inspired by Fallout-style menus, cyberpunk interfaces, Blade Runner, and Alien.

**Solution:**  
Created a RESTful API backend (Flask + Python) with environment-based configuration, paired with a terminal-themed web UI (HTML/CSS/JavaScript). Home Assistant handles the actual smart-home integrations, including Hue. The app calls Home Assistant rather than talking directly to individual device ecosystems.

**Outcome:**  
A working first pass for Home Assistant lighting control: fetch lights/scenes, activate configured scenes, turn lights on/off, and fail cleanly when Home Assistant is unavailable. Media and music are future modules.

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
3. User selects a terminal section such as `LIGHTING CONTROL`
4. Frontend fetches lighting state via `GET /api/lighting`
5. User sends a light or scene command
6. Backend checks demo mode or calls Home Assistant
6. Response returns to frontend, UI updates
7. Activity logged with timestamp

---

## Core Features

- **REST API** - Clean endpoints for lighting, scenes, legacy media, and status
- **Terminal UI** - Fallout-style menu flow with one command family visible at a time
- **Home Assistant Client** - Fetches states and calls Home Assistant service endpoints
- **Scene Shortcuts** - Configurable party scene buttons for dramatic lighting changes
- **Demo Mode** - Fully functional without Home Assistant (for testing)
- **Environment Configuration** - 12-factor app pattern, no hardcoded secrets
- **Structured Logging** - Timestamped logs for all requests and errors
- **Docker Ready** - Multi-stage Dockerfile with health checks
- **Error Handling** - Proper HTTP status codes and JSON error responses
- **Activity Log** - Command-style event tracking in the UI

---

## Technical Stack

**Languages / Runtime**
- Python 3.11 preferred
- Python 3.8+ should work for the current Flask app

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
- No Node/npm build step is required

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
LIGHT_ENTITY_ID=light.your_default_light
LIGHT_ENTITY_IDS=light.living_room,light.office_lamp
SCENE_PARTY_MODE=scene.party_mode
SCENE_MATRIX_GREEN=scene.matrix_green
SCENE_RED_ALERT=scene.red_alert
SCENE_BLACKOUT=scene.blackout
SCENE_NORMAL=scene.normal
SCENE_MAINFRAME_BREACH=scene.red_alert
FLASK_PORT=8000
```

Run the app:

```bash
python neuronodeTerminal_api.py
```

Default URL: `http://localhost:8000`

### Home Assistant Token

Create a long-lived access token in Home Assistant:

1. Open Home Assistant in your browser.
2. Click your user profile in the lower-left corner.
3. Scroll to **Long-lived access tokens**.
4. Click **Create Token**.
5. Name it something like `Neurox Terminal`.
6. Copy the token into `.env` as `HOME_ASSISTANT_TOKEN`.

The token is shown once. If you lose it, delete it and create a new one.

### Lighting Configuration

The app discovers lights from Home Assistant via `/api/states`.

Use `LIGHT_ENTITY_IDS` when you want the terminal to show only a curated list:

```env
LIGHT_ENTITY_IDS=light.living_room,light.office_lamp,light.hallway
```

Leave it blank to show every Home Assistant light entity.

Scene buttons are configured by entity ID:

```env
SCENE_RED_ALERT=scene.red_alert
SCENE_BLACKOUT=scene.blackout
SCENE_NORMAL=scene.normal
```

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
git clone https://github.com/UnchainedAtom/Neurox-Terminal.git
cd Neurox-Terminal
cp .env.example .env
nano .env
./run.sh
```

`run.sh` creates the virtual environment, installs dependencies, and starts the API. Set `FLASK_HOST=0.0.0.0` so another device on the home network can reach it, or use the Pi browser directly at `http://localhost:8000`.

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

# Lighting dashboard data
curl http://localhost:8000/api/lighting

# Turn a light on
curl -X POST http://localhost:8000/api/lights/light.overhead_light/turn-on

# Activate a configured scene
curl -X POST http://localhost:8000/api/scenes/red_alert

# Play media (returns success in demo)
curl -X POST http://localhost:8000/api/play-media
```

### Test UI

Open browser: `http://localhost:8000/`

You should see:
- Terminal-style main menu
- Lighting Control, Party Protocols, Media Relay, and System Status sections
- Large CRT-friendly commands
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
- **No advanced light controls yet** - Current scope is on/off plus scene activation
- **No authentication** - Anyone with network access can control devices
- **Demo mode only mocks responses** - It does not control real devices
- **Media playback only concept** - Media/music are future modules
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
