# 🗺️ Location Feature Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PNEUMONIA DETECTION APP                      │
│                     (enhanced_web_app.py)                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
         ┌──────────▼──────────┐   ┌─────────▼─────────┐
         │   AI Detection      │   │  Location Feature │
         │   - Upload X-ray    │   │  - Find Hospitals │
         │   - Predict         │   │  - Show Map       │
         │   - Show Results    │   │  - Get Directions │
         └─────────────────────┘   └─────────┬─────────┘
                                              │
                                   ┌──────────▼──────────┐
                                   │  LocationService    │
                                   │  (location_service) │
                                   └──────────┬──────────┘
                                              │
                        ┌─────────────────────┴─────────────────────┐
                        │                                           │
              ┌─────────▼─────────┐                    ┌───────────▼──────────┐
              │   Free APIs       │                    │   Google Maps API    │
              │   (Default)       │                    │   (Optional)         │
              ├───────────────────┤                    ├──────────────────────┤
              │ • Nominatim       │                    │ • Geocoding API      │
              │   (Geocoding)     │                    │ • Places API         │
              │ • Overpass API    │                    │ • Places Details     │
              │   (Hospitals)     │                    │                      │
              └───────────────────┘                    └──────────────────────┘
```

## User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                             │
└─────────────────────────────────────────────────────────────────┘

1. Upload X-ray Image
   │
   ▼
2. AI Analyzes Image
   │
   ▼
3. Result: PNEUMONIA DETECTED ⚠️
   │
   ▼
4. Navigate to "Find Care" Tab
   │
   ▼
5. Enter Location
   │  "New York, NY"
   │
   ▼
6. System Geocodes Address
   │  → (40.7128, -74.0060)
   │
   ▼
7. Search for Hospitals
   │  Radius: 5km
   │  Max: 10 results
   │
   ▼
8. Display Results
   │  • Interactive Map
   │  • Hospital List
   │  • Contact Info
   │
   ▼
9. User Selects Hospital
   │
   ▼
10. Get Directions / Call
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                │
└─────────────────────────────────────────────────────────────────┘

User Input: "Los Angeles, CA"
   │
   ▼
┌──────────────────────────┐
│  Geocoding Service       │
│  Input: "Los Angeles"    │
│  Output: (34.05, -118.2) │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Hospital Search         │
│  Input: Coordinates      │
│  Radius: 5000m           │
│  Output: Hospital List   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Distance Calculation    │
│  For each hospital:      │
│  - Calculate distance    │
│  - Sort by proximity     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Map Rendering           │
│  - Create Folium map     │
│  - Add markers           │
│  - Add popups            │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Display to User         │
│  - Interactive map       │
│  - Hospital cards        │
│  - Contact buttons       │
└──────────────────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENT INTERACTION                         │
└─────────────────────────────────────────────────────────────────┘

enhanced_web_app.py
│
├─ Imports LocationService
│  from src.utils.location_service import LocationService
│
├─ Imports APIConfig
│  from config.api_config import APIConfig
│
├─ Initializes Service
│  service = LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)
│
├─ User enters address
│  user_address = st.text_input("Enter location")
│
├─ Geocode address
│  coords = service.geocode_address(user_address)
│
├─ Find hospitals
│  hospitals = service.find_nearby_hospitals(coords[0], coords[1])
│
├─ Create map
│  map = create_hospital_map(coords, hospitals)
│
└─ Display results
   folium_static(map)
   for hospital in hospitals:
       display_hospital_card(hospital)
```

## API Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                      API SELECTION LOGIC                         │
└─────────────────────────────────────────────────────────────────┘

Start
  │
  ▼
Is Google Maps API key configured?
  │
  ├─ YES ──────────────────────┐
  │                            │
  │                            ▼
  │                    Use Google Maps API
  │                            │
  │                            ├─ Geocoding API
  │                            ├─ Places API
  │                            └─ Better data quality
  │
  └─ NO ───────────────────────┐
                               │
                               ▼
                    Use Free OpenStreetMap APIs
                               │
                               ├─ Nominatim (Geocoding)
                               ├─ Overpass API (Hospitals)
                               └─ Good data quality
```

## File Structure

```
project/
│
├── enhanced_web_app.py              ← Main Streamlit app
│   ├── Imports LocationService
│   ├── Imports APIConfig
│   └── Implements UI
│
├── src/
│   └── utils/
│       └── location_service.py      ← Core API logic
│           ├── LocationService class
│           ├── geocode_address()
│           ├── find_nearby_hospitals()
│           ├── _geocode_google()
│           ├── _geocode_nominatim()
│           ├── _find_hospitals_google()
│           ├── _find_hospitals_overpass()
│           └── _calculate_distance()
│
├── config/
│   └── api_config.py                ← Configuration
│       ├── GOOGLE_MAPS_API_KEY
│       ├── PLACES_SEARCH_RADIUS
│       └── MAX_RESULTS
│
├── .env                             ← Environment variables
│   └── GOOGLE_MAPS_API_KEY=...
│
├── test_location_api.py             ← Test suite
│   ├── test_api_configuration()
│   ├── test_geocoding()
│   ├── test_hospital_search()
│   └── test_distance_calculation()
│
└── examples/
    └── location_api_examples.py     ← Usage examples
        ├── example_1_address_search()
        ├── example_2_emergency_only()
        ├── example_3_closest_hospital()
        └── ...
```

## State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT STATE FLOW                          │
└─────────────────────────────────────────────────────────────────┘

Session State Variables:
│
├── st.session_state.detector
│   └── EnhancedPneumoniaDetector instance
│
├── st.session_state.result
│   └── AI prediction result
│
├── st.session_state.analyzed
│   └── Boolean: has image been analyzed?
│
└── st.session_state.user_location
    └── User's geocoded coordinates

Flow:
1. User uploads image → stored in session
2. AI analyzes → result stored in session
3. User enters location → geocoded and stored
4. Hospitals searched → displayed immediately
5. State persists across reruns
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     ERROR HANDLING                               │
└─────────────────────────────────────────────────────────────────┘

Try Geocoding
  │
  ├─ Success ──────────────────┐
  │                            │
  │                            ▼
  │                    Try Hospital Search
  │                            │
  │                            ├─ Success ────► Display Results
  │                            │
  │                            └─ Fail ───────► Show Error
  │                                             Use Sample Data
  │
  └─ Fail ─────────────────────► Show Error
                                 Use Default Location
                                 Try Again
```

## Caching Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                      CACHING LAYERS                              │
└─────────────────────────────────────────────────────────────────┘

Level 1: Service Instance
@st.cache_resource
def get_location_service():
    return LocationService()

Level 2: Geocoding Results
@st.cache_data(ttl=3600)  # 1 hour
def geocode_address(address):
    return service.geocode_address(address)

Level 3: Hospital Search
@st.cache_data(ttl=1800)  # 30 minutes
def find_hospitals(lat, lon):
    return service.find_nearby_hospitals(lat, lon)

Benefits:
- Faster response times
- Reduced API calls
- Lower costs
- Better user experience
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                               │
└─────────────────────────────────────────────────────────────────┘

1. Environment Variables
   .env file (not in Git)
   │
   ▼
2. Configuration Layer
   config/api_config.py
   │
   ▼
3. Service Layer
   src/utils/location_service.py
   │
   ▼
4. Application Layer
   enhanced_web_app.py

Security Measures:
✓ API keys in .env
✓ .env in .gitignore
✓ No hardcoded keys
✓ Environment variable fallbacks
✓ API key validation
✓ Error message sanitization
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                            │
└─────────────────────────────────────────────────────────────────┘

Option 1: Local Development
┌──────────────────────┐
│  Local Machine       │
│  - Python 3.9+       │
│  - Streamlit         │
│  - .env file         │
└──────────────────────┘

Option 2: Streamlit Cloud
┌──────────────────────┐
│  Streamlit Cloud     │
│  - GitHub repo       │
│  - Secrets in UI     │
│  - Auto-deploy       │
└──────────────────────┘

Option 3: Docker
┌──────────────────────┐
│  Docker Container    │
│  - Dockerfile        │
│  - ENV variables     │
│  - Port 8501         │
└──────────────────────┘

Option 4: Cloud Platform
┌──────────────────────┐
│  AWS/GCP/Azure       │
│  - Container service │
│  - Secrets manager   │
│  - Load balancer     │
└──────────────────────┘
```

## Performance Optimization

```
┌─────────────────────────────────────────────────────────────────┐
│                  PERFORMANCE OPTIMIZATIONS                       │
└─────────────────────────────────────────────────────────────────┘

1. Caching
   ├─ Service instance: @st.cache_resource
   ├─ Geocoding results: @st.cache_data(ttl=3600)
   └─ Hospital searches: @st.cache_data(ttl=1800)

2. Lazy Loading
   ├─ Load service only when needed
   ├─ Geocode only on user input
   └─ Search only after geocoding

3. Parallel Requests
   ├─ Use session for connection pooling
   └─ Reuse HTTP connections

4. Result Limiting
   ├─ Limit max_results to 10
   ├─ Reduce search radius when possible
   └─ Filter results client-side

5. Error Recovery
   ├─ Fallback to free APIs
   ├─ Use sample data if APIs fail
   └─ Graceful degradation
```

---

## Quick Reference

### Key Components

- **LocationService**: Core API wrapper
- **APIConfig**: Configuration management
- **enhanced_web_app.py**: UI integration
- **test_location_api.py**: Testing suite

### Key Functions

- `geocode_address(address)`: Address → Coordinates
- `find_nearby_hospitals(lat, lon)`: Coordinates → Hospitals
- `create_hospital_map()`: Hospitals → Interactive map

### Key Files

- `.env`: API keys (not in Git)
- `config/api_config.py`: Configuration
- `src/utils/location_service.py`: Core logic

### Key Concepts

- **Dual API support**: Free (OSM) + Premium (Google)
- **Graceful fallbacks**: Always works, even without API key
- **Caching**: Improves performance and reduces costs
- **Security**: API keys never in code

---

**For more details, see:**

- `README_LOCATION_FEATURE.md` - Complete documentation
- `MAP_API_SETUP_GUIDE.md` - Setup instructions
- `LOCATION_API_CHEATSHEET.md` - Quick reference
