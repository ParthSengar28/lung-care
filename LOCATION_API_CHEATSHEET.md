# 🗺️ Location API Cheat Sheet

Quick reference for the Hospital Location API

## 🚀 Quick Start

```bash
# Install
pip install -r requirements_enhanced.txt

# Run
streamlit run enhanced_web_app.py

# Test
python test_location_api.py
```

## 📝 Basic Usage

### Initialize Service

```python
from src.utils.location_service import LocationService
from config.api_config import APIConfig

# Without API key (uses free APIs)
service = LocationService()

# With Google Maps API key
service = LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)
```

### Geocode Address

```python
# Convert address to coordinates
coords = service.geocode_address("New York, NY")
# Returns: (40.7128, -74.0060) or None

# Examples of valid addresses:
coords = service.geocode_address("123 Main St, New York, NY 10001")
coords = service.geocode_address("Los Angeles, CA")
coords = service.geocode_address("90210")
coords = service.geocode_address("Times Square, New York")
```

### Find Hospitals

```python
# Find nearby hospitals
hospitals = service.find_nearby_hospitals(
    latitude=40.7128,
    longitude=-74.0060,
    radius=5000,      # meters (5km)
    max_results=10
)

# Returns list of dictionaries:
# [
#   {
#     'name': 'Hospital Name',
#     'address': '123 Main St',
#     'location': [40.7128, -74.0060],
#     'distance': 2.3,  # km
#     'phone': '555-1234',
#     'emergency': True,
#     'rating': 4.5
#   },
#   ...
# ]
```

### Complete Example

```python
# User enters address
address = "New York, NY"

# Step 1: Geocode
coords = service.geocode_address(address)

if coords:
    # Step 2: Find hospitals
    hospitals = service.find_nearby_hospitals(
        coords[0], coords[1],
        radius=5000,
        max_results=10
    )

    # Step 3: Display
    for hospital in hospitals:
        print(f"{hospital['name']} - {hospital['distance']} km")
```

## 🎯 Common Patterns

### Find Closest Hospital

```python
hospitals = service.find_nearby_hospitals(lat, lon, max_results=1)
closest = hospitals[0] if hospitals else None
```

### Filter Emergency Hospitals

```python
all_hospitals = service.find_nearby_hospitals(lat, lon, radius=10000)
emergency = [h for h in all_hospitals if h.get('emergency', True)]
```

### Sort by Distance (already sorted)

```python
hospitals = service.find_nearby_hospitals(lat, lon)
# Already sorted by distance, closest first
```

### Calculate Travel Time

```python
distance_km = hospital['distance']
avg_speed_kmh = 40
travel_time_minutes = (distance_km / avg_speed_kmh) * 60
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
GOOGLE_MAPS_API_KEY=AIzaSyD_your_key_here
PLACES_SEARCH_RADIUS=5000
MAX_RESULTS=10
```

### Python Config (config/api_config.py)

```python
APIConfig.GOOGLE_MAPS_API_KEY = 'your_key'
APIConfig.PLACES_SEARCH_RADIUS = 5000  # meters
APIConfig.MAX_RESULTS = 10
```

## 🔧 Streamlit Integration

### Basic

```python
import streamlit as st
from src.utils.location_service import LocationService

service = LocationService()

address = st.text_input("Enter location")
if address:
    coords = service.geocode_address(address)
    if coords:
        hospitals = service.find_nearby_hospitals(coords[0], coords[1])
        st.write(f"Found {len(hospitals)} hospitals")
```

### With Caching

```python
@st.cache_resource
def get_service():
    return LocationService()

@st.cache_data(ttl=3600)
def get_hospitals(lat, lon):
    service = get_service()
    return service.find_nearby_hospitals(lat, lon)

service = get_service()
address = st.text_input("Enter location")
if address:
    coords = service.geocode_address(address)
    if coords:
        hospitals = get_hospitals(coords[0], coords[1])
```

### With Map

```python
import folium
from streamlit_folium import folium_static

# Create map
m = folium.Map(location=[lat, lon], zoom_start=13)

# Add markers
for hospital in hospitals:
    folium.Marker(
        hospital['location'],
        popup=hospital['name'],
        tooltip=f"{hospital['distance']} km"
    ).add_to(m)

# Display
folium_static(m)
```

## 🐛 Error Handling

### Check if Geocoding Succeeded

```python
coords = service.geocode_address(address)
if coords:
    # Success
    lat, lon = coords
else:
    # Failed - use default or show error
    st.error("Could not find location")
```

### Check if Hospitals Found

```python
hospitals = service.find_nearby_hospitals(lat, lon)
if hospitals:
    # Display hospitals
    for h in hospitals:
        st.write(h['name'])
else:
    # No hospitals found
    st.warning("No hospitals found in this area")
```

### Try-Except Pattern

```python
try:
    coords = service.geocode_address(address)
    if coords:
        hospitals = service.find_nearby_hospitals(coords[0], coords[1])
        return hospitals
except Exception as e:
    st.error(f"Error: {str(e)}")
    return []
```

## 📊 API Comparison

| Feature   | Free (OSM) | Google Maps  |
| --------- | ---------- | ------------ |
| Cost      | $0         | $200/mo free |
| Setup     | None       | API key      |
| Geocoding | ✅         | ✅ Better    |
| Hospitals | ✅         | ✅ Better    |
| Ratings   | ❌         | ✅           |
| Reviews   | ❌         | ✅           |
| Limits    | 1/sec      | 1000s/sec    |

## 🧪 Testing

### Test Geocoding

```bash
python -c "from src.utils.location_service import LocationService; \
           s = LocationService(); \
           print(s.geocode_address('New York, NY'))"
```

### Test Hospital Search

```bash
python -c "from src.utils.location_service import LocationService; \
           s = LocationService(); \
           h = s.find_nearby_hospitals(40.7128, -74.0060); \
           print(f'Found {len(h)} hospitals')"
```

### Run Full Test Suite

```bash
python test_location_api.py
```

## 🔑 Google Maps Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project
3. Enable APIs:
   - Geocoding API
   - Places API
4. Create API key
5. Add to `.env`:
   ```bash
   GOOGLE_MAPS_API_KEY=AIzaSyD_your_key_here
   ```

## 💡 Tips

### Performance

- Cache results with `@st.cache_data`
- Reduce search radius for faster results
- Limit max_results to what you need

### Accuracy

- Use specific addresses for better geocoding
- Include city and state
- Use Google Maps API for best results

### Security

- Never commit API keys to Git
- Use environment variables
- Add `.env` to `.gitignore`

### Debugging

- Print coordinates to verify geocoding
- Check if hospitals list is empty
- Run test script to verify setup
- Check API quotas in Google Cloud Console

## 📚 Resources

- **Setup Guide**: `MAP_API_SETUP_GUIDE.md`
- **Quick Start**: `LOCATION_API_QUICK_START.md`
- **Full Docs**: `README_LOCATION_FEATURE.md`
- **Examples**: `examples/location_api_examples.py`
- **Tests**: `test_location_api.py`

## 🆘 Common Issues

### "No hospitals found"

→ Increase radius or try different location

### "Geocoding failed"

→ Use more specific address with city/state

### "Rate limit exceeded"

→ Add delays or upgrade to Google Maps API

### "API key not valid"

→ Check key in Google Cloud Console, ensure APIs enabled

## ✅ Quick Checklist

- [ ] Install: `pip install -r requirements_enhanced.txt`
- [ ] Test: `python test_location_api.py`
- [ ] Run: `streamlit run enhanced_web_app.py`
- [ ] (Optional) Add Google Maps API key to `.env`

---

**Need more help?** See full documentation in `README_LOCATION_FEATURE.md`
