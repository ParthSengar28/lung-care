"""
Location Service for Finding Nearby Hospitals
Supports multiple APIs: Google Places, OpenStreetMap (Nominatim)
"""
import requests
import json
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class LocationService:
    """Service for geocoding and finding nearby hospitals"""
    
    def __init__(self, google_api_key: Optional[str] = None):
        self.google_api_key = google_api_key
        self.session = requests.Session()
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert address to coordinates (latitude, longitude)
        Uses Google Geocoding API if available, otherwise Nominatim (free)
        """
        if self.google_api_key and self.google_api_key != 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
            return self._geocode_google(address)
        else:
            return self._geocode_nominatim(address)
    
    def _geocode_google(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode using Google Geocoding API"""
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': address,
                'key': self.google_api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                location = data['results'][0]['geometry']['location']
                return (location['lat'], location['lng'])
            else:
                logger.warning(f"Google Geocoding failed: {data.get('status')}")
                return None
                
        except Exception as e:
            logger.error(f"Google geocoding error: {str(e)}")
            return None
    
    def _geocode_nominatim(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode using OpenStreetMap Nominatim (free, no API key required)"""
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': 'PneumoniaDetectionApp/1.0'
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                return (float(data[0]['lat']), float(data[0]['lon']))
            else:
                logger.warning("Nominatim geocoding returned no results")
                return None
                
        except Exception as e:
            logger.error(f"Nominatim geocoding error: {str(e)}")
            return None
    
    def find_nearby_hospitals(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int = 5000,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Find nearby hospitals using available API
        """
        if self.google_api_key and self.google_api_key != 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
            return self._find_hospitals_google(latitude, longitude, radius, max_results)
        else:
            return self._find_hospitals_overpass(latitude, longitude, radius, max_results)
    
    def _find_hospitals_google(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int,
        max_results: int
    ) -> List[Dict]:
        """Find hospitals using Google Places API"""
        try:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                'location': f"{latitude},{longitude}",
                'radius': radius,
                'type': 'hospital',
                'key': self.google_api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK':
                hospitals = []
                for place in data['results'][:max_results]:
                    hospital = {
                        'name': place.get('name', 'Unknown Hospital'),
                        'address': place.get('vicinity', 'Address not available'),
                        'location': [
                            place['geometry']['location']['lat'],
                            place['geometry']['location']['lng']
                        ],
                        'rating': place.get('rating', 0),
                        'open_now': place.get('opening_hours', {}).get('open_now', None),
                        'place_id': place.get('place_id', ''),
                        'distance': self._calculate_distance(
                            latitude, longitude,
                            place['geometry']['location']['lat'],
                            place['geometry']['location']['lng']
                        )
                    }
                    hospitals.append(hospital)
                
                # Sort by distance
                hospitals.sort(key=lambda x: x['distance'])
                return hospitals
            else:
                logger.warning(f"Google Places API failed: {data.get('status')}")
                return []
                
        except Exception as e:
            logger.error(f"Google Places API error: {str(e)}")
            return []
    
    def _find_hospitals_overpass(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int,
        max_results: int
    ) -> List[Dict]:
        """Find hospitals using OpenStreetMap Overpass API (free, no API key)"""
        try:
            # Overpass API query for hospitals
            overpass_url = "https://overpass-api.de/api/interpreter"
            
            query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="hospital"](around:{radius},{latitude},{longitude});
              way["amenity"="hospital"](around:{radius},{latitude},{longitude});
              relation["amenity"="hospital"](around:{radius},{latitude},{longitude});
            );
            out center;
            """
            
            response = self.session.post(overpass_url, data={'data': query}, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            hospitals = []
            for element in data.get('elements', [])[:max_results]:
                # Get coordinates
                if element['type'] == 'node':
                    lat, lon = element['lat'], element['lon']
                else:
                    # For ways and relations, use center
                    lat = element.get('center', {}).get('lat', latitude)
                    lon = element.get('center', {}).get('lon', longitude)
                
                tags = element.get('tags', {})
                
                hospital = {
                    'name': tags.get('name', 'Hospital'),
                    'address': self._format_osm_address(tags),
                    'location': [lat, lon],
                    'phone': tags.get('phone', 'N/A'),
                    'emergency': tags.get('emergency') == 'yes',
                    'distance': self._calculate_distance(latitude, longitude, lat, lon)
                }
                hospitals.append(hospital)
            
            # Sort by distance
            hospitals.sort(key=lambda x: x['distance'])
            return hospitals
            
        except Exception as e:
            logger.error(f"Overpass API error: {str(e)}")
            return []
    
    def _format_osm_address(self, tags: Dict) -> str:
        """Format address from OSM tags"""
        parts = []
        
        if 'addr:housenumber' in tags:
            parts.append(tags['addr:housenumber'])
        if 'addr:street' in tags:
            parts.append(tags['addr:street'])
        if 'addr:city' in tags:
            parts.append(tags['addr:city'])
        
        if parts:
            return ', '.join(parts)
        else:
            return tags.get('addr:full', 'Address not available')
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers using Haversine formula"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        distance = R * c
        return round(distance, 2)
    
    def get_hospital_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information about a hospital (Google Places only)"""
        if not self.google_api_key or self.google_api_key == 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
            return None
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,formatted_phone_number,opening_hours,website,rating,reviews',
                'key': self.google_api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK':
                return data['result']
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting hospital details: {str(e)}")
            return None
