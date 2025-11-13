"""
API Configuration for Map Location Services
Store your API keys here (use environment variables in production)
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIConfig:
    """Configuration for external APIs"""
    
    # Google Maps/Places API
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_MAPS_API_KEY_HERE')
    
    # OpenCage Geocoding API (alternative for geocoding)
    OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY', 'YOUR_OPENCAGE_API_KEY_HERE')
    
    # Mapbox API (alternative mapping service)
    MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', 'YOUR_MAPBOX_API_KEY_HERE')
    
    # API Settings
    PLACES_SEARCH_RADIUS = 5000  # meters (5km)
    MAX_RESULTS = 10
    
    @classmethod
    def is_google_maps_configured(cls):
        """Check if Google Maps API is configured"""
        return cls.GOOGLE_MAPS_API_KEY and cls.GOOGLE_MAPS_API_KEY != 'YOUR_GOOGLE_MAPS_API_KEY_HERE'
    
    @classmethod
    def is_opencage_configured(cls):
        """Check if OpenCage API is configured"""
        return cls.OPENCAGE_API_KEY and cls.OPENCAGE_API_KEY != 'YOUR_OPENCAGE_API_KEY_HERE'
