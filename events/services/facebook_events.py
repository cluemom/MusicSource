# services/facebook_events.py
import requests
from datetime import datetime, timedelta

def fetch_facebook_events(api_service):
    # todo:finish this
    if not api_service.is_active:
        return []

    endpoint = api_service.endpoint_url
    client_id = api_service.client_id
    keyword = api_service.keyword
    location = api_service.location
    radius = api_service.radius
    time_frame = api_service.time_frame_weeks

    # Define query parameters
    params = {
        "access_token": client_id,
        "q": keyword,
        "type": "event",
        "center": location,
        "distance": radius * 1609,  # Convert miles to meters
        "since": int(datetime.now().timestamp()),  # Current time
        "until": int((datetime.now() + timedelta(weeks=time_frame)).timestamp()),  # 3 weeks ahead
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.RequestException as e:
        print(f"Error fetching Facebook events: {e}")
        return []
