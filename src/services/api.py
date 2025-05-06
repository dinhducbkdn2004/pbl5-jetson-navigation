"""
API service module for communication with navigation backend
"""
import requests
from src.config.settings import API_URL

class APIService:
    def __init__(self, api_url=API_URL):
        self.api_url = api_url
        
    def get_navigation_route(self, latitude, longitude, destination):
        """
        Request navigation route from API
        
        Args:
            latitude (float): Current latitude
            longitude (float): Current longitude
            destination (str): Destination text
            
        Returns:
            dict: Response data or None if request failed
        """
        data = {
            "current_location": {"latitude": latitude, "longitude": longitude},
            "destination_text": destination
        }
        print(f"API Request Payload: {data}")
        
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            print("📡 Response data from API:", response.json())
            return response.json()
        except Exception as e:
            print(f"Error sending API request: {e}")
            return None