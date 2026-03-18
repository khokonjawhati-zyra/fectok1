import requests
import json

url = "http://127.0.0.1:5000/api/v15/register_media"
payload = {
    "file": "grok_video_2026-02-22-15-06-12_1772723919.mp4",
    "uploader": "SOV_AUTO_TEST",
    "desc": "Manual Registration Test Pulse",
    "thumbnail": "grok_video_2026-02-22-15-06-12_1772723919.jpg",
    "sound": "s_test.mp3",
    "sound_status": "SAFE",
    "sound_name": "Original Sound - SOV_AUTO_TEST",
    "sound_url": "",
    "original_volume": 1.0,
    "added_sound_volume": 0.5,
    "location": "TEST_ZONE",
    "hls_ready": False
}

try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Raw: {response.text[:200]}")
    try:
        print(f"Response: {response.json()}")
    except:
        print("Response is not JSON")
except Exception as e:
    print(f"Error: {e}")
