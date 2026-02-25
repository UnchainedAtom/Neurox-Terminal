# Neurox Terminal

A Flask-based REST API for controlling smart home devices via Home Assistant. Designed as a terminal-style interface for Raspberry Pi, with built-in demo mode for testing without a live Home Assistant instance.

## Features

- **RESTful API** - Clean, modern API endpoints for device control
- **Home Assistant Integration** - Full integration with Home Assistant API
- **Demo Mode** - Built-in demo/mock mode for testing without external dependencies
- **Environment Configuration** - 12-factor app configuration via environment variables
- **Comprehensive Logging** - Detailed logging for debugging and monitoring
- **Error Handling** - Robust error handling with informative responses
- **Docker Support** - Production-ready Dockerfile with health checks
- **Documentation** - Well-documented code and API endpoints

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

- Python 3.8+
- Home Assistant (optional - demo mode works without it)
- pip or pip3

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/UnchainedAtom/Neurox-Terminal.git
cd Neurox-Terminal
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv neuroxnodeTerminal-venv
source neuroxnodeTerminal-venv/bin/activate  # On Windows: neuroxnodeTerminal-venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` and update values:

```env
# Home Assistant Configuration
HOME_ASSISTANT_URL=http://your-homeassistant-instance:8123
HOME_ASSISTANT_TOKEN=your_long_lived_access_token_here

# Entity Configuration
LIGHT_ENTITY_ID=light.your_light_entity

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Demo Mode (set to True for testing without Home Assistant)
DEMO_MODE=False
```

## Running the Application

### Development Mode (Local)

```bash
python neuronodeTerminal_api.py
```

The API will be available at `http://localhost:5000`

### Demo Mode (No Home Assistant Required)

For testing without a live Home Assistant instance:

```env
DEMO_MODE=True
```

### Production with Docker

Build the Docker image:

```bash
docker build -t neurox-terminal .
```

Run the container:

```bash
docker run -p 5000:5000 \
  -e HOME_ASSISTANT_URL=http://homeassistant:8123 \
  -e HOME_ASSISTANT_TOKEN=your_token \
  -e LIGHT_ENTITY_ID=light.your_light \
  neurox-terminal
```

Or with environment file:

```bash
docker run -p 5000:5000 --env-file .env neurox-terminal
```

### On Raspberry Pi

Using the provided startup script:

```bash
./run.sh
```

(Update paths in `run.sh` as needed for your setup)

## API Documentation

### Health Check

**GET** `/`

Returns service status.

```bash
curl http://localhost:5000/
```

Response:
```json
{
  "status": "running",
  "service": "Neurox Terminal API",
  "demo_mode": false,
  "message": "Neuroxnode API is running"
}
```

### Status Endpoint

**GET** `/api/status`

Returns detailed status information.

```bash
curl http://localhost:5000/api/status
```

Response:
```json
{
  "status": "operational",
  "demo_mode": false,
  "home_assistant_configured": true,
  "endpoints": [
    "/api/toggle-lights",
    "/api/play-media",
    "/api/status"
  ]
}
```

### Toggle Lights

**POST** `/api/toggle-lights`

Toggle the configured light entity.

```bash
curl -X POST http://localhost:5000/api/toggle-lights
```

Response (Success):
```json
{
  "status": "success",
  "response": {...}
}
```

Response (Demo Mode):
```json
{
  "status": "success",
  "demo": true,
  "message": "Lights toggled (demo mode)"
}
```

### Play Media

**POST** `/api/play-media`

Play media file via VLC.

```bash
curl -X POST http://localhost:5000/api/play-media
```

Response:
```json
{
  "status": "success",
  "message": "media playing"
}
```

## Configuration Details

### Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `HOME_ASSISTANT_URL` | `http://localhost:8123` | No | Home Assistant base URL |
| `HOME_ASSISTANT_TOKEN` | (empty) | Yes* | Home Assistant long-lived access token (*not required in demo mode) |
| `LIGHT_ENTITY_ID` | `light.overhead_light` | No | Home Assistant light entity ID |
| `MEDIA_PATH` | `/home/pi/media.mp4` | No | Path to media file |
| `FLASK_HOST` | `0.0.0.0` | No | Flask server bind address |
| `FLASK_PORT` | `5000` | No | Flask server port |
| `FLASK_ENV` | `development` | No | Flask environment (`development` or `production`) |
| `FLASK_DEBUG` | `False` | No | Enable Flask debug mode |
| `DEMO_MODE` | `False` | No | Enable demo/mock mode (no Home Assistant required) |

### Home Assistant Setup

To get your Home Assistant token:

1. Log in to Home Assistant
2. Go to Profile (bottom left)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Copy the token and add to `.env` file

## Logging

The application provides detailed logging for debugging and monitoring:

```
2025-02-25 10:30:45,123 - app.routes - INFO - Light toggle request received
2025-02-25 10:30:45,234 - app.controller - INFO - Toggling light: light.overhead_light
2025-02-25 10:30:45,450 - app.controller - INFO - Light toggled successfully
```

Configure log level via environment variable or code modifications.

## Testing with Demo Mode

The easiest way to test the API without Home Assistant:

1. **Enable Demo Mode:**
   ```env
   DEMO_MODE=True
   ```

2. **Start the application:**
   ```bash
   python neuronodeTerminal_api.py
   ```

3. **Test endpoints:**
   ```bash
   # Test health
   curl http://localhost:5000/

   # Test light toggle (will return success in demo mode)
   curl -X POST http://localhost:5000/api/toggle-lights

   # Test media playback (will return success in demo mode)
   curl -X POST http://localhost:5000/api/play-media
   ```

## Deployment Recommendations

### Raspberry Pi Deployment

1. Use systemd service for auto-start:
   ```bash
   sudo systemctl enable neurox-terminal
   sudo systemctl start neurox-terminal
   ```

2. Configure reverse proxy with nginx:
   ```nginx
   server {
       listen 80;
       server_name neurox-terminal.local;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
       }
   }
   ```

### Docker Deployment

Use Docker Compose for local/dev deployments:

```yaml
version: '3.8'
services:
  neurox-terminal:
    build: .
    ports:
      - "5000:5000"
    environment:
      - HOME_ASSISTANT_URL=http://homeassistant:8123
      - HOME_ASSISTANT_TOKEN=${HA_TOKEN}
      - DEMO_MODE=False
    depends_on:
      - homeassistant
```

## Future Enhancements

- [ ] Web UI Dashboard
- [ ] Additional device types (switches, thermostats, sensors)
- [ ] User authentication & authorization
- [ ] Automation scheduling
- [ ] Event webhooks from Home Assistant
- [ ] MQTT support
- [ ] Historical data storage
- [ ] Multi-user support

## Troubleshooting

### Home Assistant Connection Issues

**Problem:** "Failed to connect to Home Assistant"

**Solutions:**
- Verify `HOME_ASSISTANT_URL` is correct and accessible
- Check that `HOME_ASSISTANT_TOKEN` is valid (recreate if necessary)
- Ensure firewall allows connections to port 8123
- Test with `curl`: `curl -H "Authorization: Bearer YOUR_TOKEN" http://your-ha:8123/api/`

### Missing Dependencies

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
Change the port in `.env`:
```env
FLASK_PORT=5001
```

## License

MIT License - Feel free to use this project as a portfolio piece or for personal use.

## Author

UnchainedAtom

## Contributing

This is primarily a personal portfolio project, but suggestions and improvements are welcome!