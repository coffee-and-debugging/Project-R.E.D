import requests
from django.conf import settings

class LocationService:
    @staticmethod
    def get_address_from_coordinates(lat, lng):
        """Get address from coordinates using reverse geocoding"""
        try:
            url = f"https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lng,
                'format': 'json'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('display_name', f"Lat: {lat}, Lng: {lng}")
        except Exception as e:
            print(f"Reverse geocoding failed: {e}")
        
        return f"Lat: {lat}, Lng: {lng}"

    @staticmethod
    def get_coordinates_from_address(address):
        """Get coordinates from address using geocoding"""
        try:
            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]['lat']), float(data[0]['lon'])
        except Exception as e:
            print(f"Geocoding failed: {e}")
        
        return None, None
