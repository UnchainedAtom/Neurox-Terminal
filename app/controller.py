import os
import requests

HOME_ASSISTANT_URL = 'http://neuroxnode-terminal:8123'  # or your Pi's IP
ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3NDE4MTY5YWQyNTA0Yjc2YjFlOTMwN2E1YTM2MTNkZiIsImlhdCI6MTc0OTE4MzIxNCwiZXhwIjoyMDY0NTQzMjE0fQ.bDD5W9vxjgBN343prt6vX_RSsUNyWjZ5SPaZRBo-mpU'
ENTITY_ID = 'light.overhead_light'  # Replace with your real one

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def toggle_lights():
    url = f"{HOME_ASSISTANT_URL}/api/services/light/toggle"
    payload = {"entity_id": ENTITY_ID}
    print("Lights toggled!")
    response = requests.post(url, json=payload, headers=headers)
    return response

def play_media():
    os.system("vlc /home/pi/media.mp4 &")
    return "media playing"