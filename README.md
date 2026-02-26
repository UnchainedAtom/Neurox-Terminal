# Neurox Terminal

A Flask API for controlling smart home devices through Home Assistant. Originally built for a Raspberry Pi with a terminal vibe—complete with the glowing retro aesthetic.

## What it does

- **REST API** - Simple endpoints to toggle lights and control media
- **Home Assistant integration** - Talks directly to your Home Assistant instance
- **Demo mode** - Works without Home Assistant so you can actually test it
- **Configuration via environment variables** - No hardcoded credentials (secure by default)
- **Actually logs things** - Timestamps, errors, everything you'd need to debug
- **Docker ready** - Build and run in a container, health checks included
- **Comes with a dashboard** - Web UI with that retro terminal aesthetic

## Architecture

```
Neurox Terminal API
├── app/
│   ├── config.py      # Configuration management
│   ├── controller.py   # Business logic & device control
│   ├── routes.py      # Flask routes & API endpoints
│   └── __init__.py
├── neuronodeTerminal_api.py  # Application entry point
├── requirements.txt   # Python dependencies
├── Dockerfile        # Docker container definition
├── .env.example      # Environment configuration template
└── run.sh           # Bash startup script for Raspberry Pi
```

## Prerequisites

- Python 3.8 or newer
- Home Assistant (optional—demo mode works without it)
- pip

## Setup

Clone it:

```bash
git clone https://github.com/UnchainedAtom/Neurox-Terminal.git
cd Neurox-Terminal
```

Create a virtual environment (you should):

```bash
python3 -m venv neuroxnodeTerminal-venv
source neuroxnodeTerminal-venv/bin/activate  # Windows: neuroxnodeTerminal-venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up your environment:

```bash
cp .env.example .env
```

Edit the `.env` file with your setup:

```env
# If you have Home Assistant
HOME_ASSISTANT_URL=http://your-homeassistant-instance:8123
HOME_ASSISTANT_TOKEN=your_long_lived_access_token_here
LIGHT_ENTITY_ID=light.your_light

# Or just run in demo mode (no Home Assistant needed)
DEMO_MODE=True
```

## Running it

Start the API:

```bash
python neuronodeTerminal_api.py
```

It'll be available at `http://localhost:8000`

To test without Home Assistant, just make sure `DEMO_MODE=True` in your `.env` and everything works. All endpoints return success responses so you can test the whole flow.

### Docker (if you prefer containers)

```bash
docker-compose up
```

Or build and run manually:

```bash
docker build -t neurox-terminal .
docker run -p 8000:8000 -e DEMO_MODE=True neurox-terminal
```

### On Raspberry Pi

```bash
./run.sh
```

It'll create the venv, install dependencies, and start the API. Just edit paths in the script if needed.

## API Endpoints

### GET `/`

Main dashboard UI. Open in a browser to see the control panel.

### GET `/api/status`

Check if the API is alive and what mode it's in.

```bash
curl http://localhost:8000/api/status
```

```json
{
  "status": "operational",
  "demo_mode": true,
  "home_assistant_configured": false,
  "endpoints": ["/api/toggle-lights", "/api/play-media", "/api/status"]
}
```

### POST `/api/toggle-lights`

Toggle the lights.

```bash
curl -X POST http://localhost:8000/api/toggle-lights
```

Returns `{"status": "success"}` in demo mode, or talks to Home Assistant if configured.

### POST `/api/play-media`

Start media playback (via VLC or Home Assistant).

```bash
curl -X POST http://localhost:8000/api/play-media
```

Same responses as above.

## Configuration

These go in your `.env` file:

- `DEMO_MODE` - Set to `True` to run without Home Assistant (useful for testing)
- `HOME_ASSISTANT_URL` - Where your Home Assistant is running (e.g., `http://homeassistant.local:8123`)
- `HOME_ASSISTANT_TOKEN` - Long-lived access token from Home Assistant
- `LIGHT_ENTITY_ID` - The light you want to control (e.g., `light.bedroom`)
- `MEDIA_PATH` - Path to your media file (if using VLC)
- `FLASK_PORT` - What port to run on (default: 8000)
- `FLASK_DEBUG` - Set to `True` for dev, `False` for production

### Getting your Home Assistant token

1. Log into Home Assistant
2. Click your profile (bottom left)
3. Scroll down to "Long-Lived Access Tokens"
4. Create one and paste it in `.env`

## Logging & Debugging

The app logs everything to console with timestamps. Useful for debugging when things go wrong:

```
2026-02-25 18:07:40 - app.routes - INFO - Light toggle request received
2026-02-25 18:07:40 - app.controller - INFO - DEMO MODE: Lights toggled (virtual)
2026-02-25 18:07:40 - werkzeug - INFO - 127.0.0.1 - "POST /api/toggle-lights HTTP/1.1" 200
```

Set `FLASK_DEBUG=True` in `.env` for more verbose output during development.

## Testing

The easiest way to test everything is with demo mode. No Home Assistant needed:

```bash
# Make sure .env has:
DEMO_MODE=True

# Start it:
python neuronodeTerminal_api.py

# In another terminal, test:
curl http://localhost:8000/
curl -X POST http://localhost:8000/api/toggle-lights
curl -X POST http://localhost:8000/api/play-media
```

All endpoints return success responses in demo mode, so you can see the whole flow works without any actual hardware.

## Deployment

### On a Raspberry Pi

Just run the script:

```bash
./run.sh
```

For auto-start on boot, use systemd or cron.

### With Docker

Simplest:

```bash
docker-compose up
```

Or build it yourself:

```bash
docker build -t neurox-terminal .
docker run -p 8000:8000 -e DEMO_MODE=True neurox-terminal
```

### Reverse proxy (nginx)

If you want it accessible at a domain:

```nginx
server {
    listen 80;
    server_name home.local;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

## What's next?

Things I'd like to add eventually:

- More device types (switches, thermostats, etc.)
- Better UI with more controls
- Auth/user support
- Scheduling/automation
- Webhooks from Home Assistant
- MQTT support
- Data history/graphs

## Troubleshooting

### Can't connect to Home Assistant?

- Make sure the URL is correct and you can ping it
- Check that your token is still valid (recreate if needed)
- Verify firewall isn't blocking port 8123

### `ModuleNotFoundError`?

```bash
pip install -r requirements.txt
```

### Port already in use?

Change it in `.env`:

```env
FLASK_PORT=8001
```

### It still doesn't work?

Check the logs—they're printed to console. Look for error messages with timestamps.

## License

MIT - Use it however you want.

## Author

UnchainedAtom

## Contributing

This started as a personal project for my Raspberry Pi. If you have ideas or improvements, feel free to open an issue or PR!