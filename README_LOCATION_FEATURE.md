# 🗺️ Hospital Location Feature - Complete Guide

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [API Options](#api-options)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The Hospital Location Feature allows users to find nearby healthcare facilities based on their location. It integrates seamlessly with the Pneumonia Detection AI to provide a complete healthcare solution.

### What It Does:

- 📍 Converts addresses to coordinates (geocoding)
- 🏥 Finds nearby hospitals within a specified radius
- 📏 Calculates distances to each hospital
- 🗺️ Displays results on an interactive map
- 📞 Provides contact information
- ⭐ Shows ratings and reviews (with Google API)

### Why It's Useful:

When the AI detects pneumonia, users need to know where to seek medical care. This feature provides that critical information instantly.

---

## ⚡ Quick Start

### Option 1: Use Free APIs (No Setup)

```bash
# 1. Install dependencies
pip install -r requirements_enhanced.txt

# 2. Run the application
streamlit run enhanced_web_app.py

# 3. Navigate to "Find Care" tab
# 4. Enter a location
# 5. See nearby hospitals!
```

**That's it!** The app works immediately using free OpenStreetMap APIs.

### Option 2: Add Google Maps API (Better Results)

```bash
# 1. Get API key from Google Cloud Console
#    https://console.cloud.google.com/

# 2. Create .env file
echo "GOOGLE_MAPS_API_KEY=AIzaSyD_your_key_here" > .env

# 3. Run the application
streamlit run enhanced_web_app.py
```

See [MAP_API_SETUP_GUIDE.md](MAP_API_SETUP_GUIDE.md) for detailed Google Maps setup.

---

## ✨ Features

### 1. Geocoding

Convert any address format to coordinates:

- Full addresses: "123 Main St, New York, NY 10001"
- City names: "Los Angeles, CA"
- Zip codes: "90210"
- Landmarks: "Times Square, New York"

### 2. Hospital Search

Find hospitals with customizable parameters:

- Search radius (default: 5km)
- Maximum results (default: 10)
- Filter by emergency services
- Sort by distance

### 3. Interactive Map

- User location marker (red)
- Hospital markers (color-coded)
- Popup information windows
- Zoom and pan controls
- Multiple map styles

### 4. Hospital Information

- Name and address
- Phone number
- Distance from user
- Emergency services indicator
- Ratings and reviews (Google API)
- Operating hours (Google API)

### 5. Smart Fallbacks

- Automatically uses free APIs if no key configured
- Falls back to sample data if APIs fail
- Graceful error handling
- User-friendly error messages

---

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────┐
│         enhanced_web_app.py             │
│         (Streamlit Interface)           │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│    src/utils/location_service.py        │
│    (Location Service Layer)             │
└──────────────┬──────────────────────────┘
               │
               ↓
┌──────────────┴──────────────────────────┐
│                                          │
│  ┌────────────────┐  ┌────────────────┐ │
│  │  Google Maps   │  │  OpenStreetMap │ │
│  │  - Geocoding   │  │  - Nominatim   │ │
│  │  - Places API  │  │  - Overpass    │ │
│  └────────────────┘  └────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

### File Structure

```
project/
├── src/
│   └── utils/
│       └── location_service.py      # Main API service
├── config/
│   └── api_config.py                # Configuration
├── examples/
│   └── location_api_examples.py     # Usage examples
├── enhanced_web_app.py              # Streamlit app (updated)
├── test_location_api.py             # Test suite
├── .env.example                     # Environment template
├── MAP_API_SETUP_GUIDE.md          # Setup guide
├── LOCATION_API_QUICK_START.md     # Quick reference
└── README_LOCATION_FEATURE.md      # This file
```

---

## 🔌 API Options

### Free APIs (Default)

#### OpenStreetMap Nominatim

- **Purpose**: Geocoding (address → coordinates)
- **Cost**: Free
- **Limits**: 1 request/second
- **Coverage**: Worldwide
- **Setup**: None required

#### Overpass API

- **Purpose**: Finding hospitals
- **Cost**: Free
- **Limits**: Fair use policy
- **Coverage**: Worldwide
- **Setup**: None required

### Premium APIs

#### Google Maps Platform

- **APIs Used**:
  - Geocoding API
  - Places API (Nearby Search)
  - Places API (Details)
- **Cost**: $200/month free credit
- **Limits**: High (1000s requests/second)
- **Coverage**: Worldwide
- **Setup**: API key required

#### Comparison

| Feature           | Free (OSM) | Google Maps  |
| ----------------- | ---------- | ------------ |
| **Cost**          | $0         | $200/mo free |
| **Setup Time**    | 0 minutes  | 15 minutes   |
| **Geocoding**     | Good       | Excellent    |
| **Hospital Data** | Good       | Excellent    |
| **Ratings**       | ❌         | ✅           |
| **Reviews**       | ❌         | ✅           |
| **Photos**        | ❌         | ✅           |
| **Hours**         | Limited    | ✅           |
| **Real-time**     | ❌         | ✅           |
| **Rate Limits**   | 1/sec      | 1000s/sec    |

---

## 💻 Usage Examples

### Example 1: Basic Usage

```python
from src.utils.location_service import LocationService

# Initialize service
service = LocationService()

# Find hospitals near coordinates
hospitals = service.find_nearby_hospitals(
    latitude=40.7128,
    longitude=-74.0060,
    radius=5000,
    max_results=10
)

# Display results
for hospital in hospitals:
    print(f"{hospital['name']}")
    print(f"  Distance: {hospital['distance']} km")
    print(f"  Address: {hospital['address']}")
    print()
```

### Example 2: Geocode Address First

```python
# User enters address
user_address = "1600 Amphitheatre Parkway, Mountain View, CA"

# Convert to coordinates
coords = service.geocode_address(user_address)

if coords:
    # Find nearby hospitals
    hospitals = service.find_nearby_hospitals(
        coords[0], coords[1],
        radius=5000
    )
    print(f"Found {len(hospitals)} hospitals")
```

### Example 3: Find Closest Hospital

```python
# Get all nearby hospitals
hospitals = service.find_nearby_hospitals(lat, lon, radius=10000)

# They're already sorted by distance
closest = hospitals[0]

print(f"Closest hospital: {closest['name']}")
print(f"Distance: {closest['distance']} km")
print(f"Phone: {closest['phone']}")
```

### Example 4: Filter Emergency Hospitals

```python
# Find all hospitals
all_hospitals = service.find_nearby_hospitals(lat, lon, radius=10000)

# Filter for emergency services
emergency_hospitals = [
    h for h in all_hospitals
    if h.get('emergency', True)
]

print(f"Found {len(emergency_hospitals)} emergency hospitals")
```

### Example 5: Streamlit Integration

```python
import streamlit as st
from src.utils.location_service import LocationService

# Initialize service (cached)
@st.cache_resource
def get_service():
    return LocationService()

service = get_service()

# User input
address = st.text_input("Enter your location")

if address:
    # Geocode
    coords = service.geocode_address(address)

    if coords:
        # Search
        hospitals = service.find_nearby_hospitals(
            coords[0], coords[1]
        )

        # Display
        for hospital in hospitals:
            st.write(f"🏥 {hospital['name']}")
            st.write(f"📏 {hospital['distance']} km")
```

More examples in [examples/location_api_examples.py](examples/location_api_examples.py)

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Google Maps API (optional)
GOOGLE_MAPS_API_KEY=AIzaSyD_your_key_here

# Search parameters
PLACES_SEARCH_RADIUS=5000
MAX_RESULTS=10
```

### Python Configuration (config/api_config.py)

```python
class APIConfig:
    # API Keys
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

    # Search Settings
    PLACES_SEARCH_RADIUS = 5000  # meters
    MAX_RESULTS = 10

    # Timeouts
    REQUEST_TIMEOUT = 10  # seconds
```

### Customization Options

```python
# Change search radius
APIConfig.PLACES_SEARCH_RADIUS = 10000  # 10km

# Change max results
APIConfig.MAX_RESULTS = 20

# Use different API
service = LocationService(google_api_key='your_key')
```

---

## 🧪 Testing

### Run Test Suite

```bash
python test_location_api.py
```

### Expected Output

```
🔧 API Configuration Test
✓ Google Maps API configured: False
ℹ️  No Google Maps API key - will use free OpenStreetMap APIs
✓ Search radius: 5000 meters
✓ Max results: 10

📍 Geocoding Test
🔍 Testing: New York, NY
   ✅ Success: 40.7128, -74.0060

🏥 Hospital Search Test
✅ Found 5 hospitals:
   1. NewYork-Presbyterian Hospital
      📍 525 E 68th St, New York
      📏 2.3 km

📏 Distance Calculation Test
✅ Distance calculation accurate!

✅ All tests completed!
```

### Manual Testing

1. **Test Geocoding**:

   ```python
   python -c "from src.utils.location_service import LocationService; \
              s = LocationService(); \
              print(s.geocode_address('New York, NY'))"
   ```

2. **Test Hospital Search**:

   ```python
   python -c "from src.utils.location_service import LocationService; \
              s = LocationService(); \
              h = s.find_nearby_hospitals(40.7128, -74.0060); \
              print(f'Found {len(h)} hospitals')"
   ```

3. **Test in Web App**:
   - Run: `streamlit run enhanced_web_app.py`
   - Go to "Find Care" tab
   - Enter: "New York, NY"
   - Verify hospitals appear on map

---

## 🚀 Deployment

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements_enhanced.txt

# 2. (Optional) Configure API key
echo "GOOGLE_MAPS_API_KEY=your_key" > .env

# 3. Run
streamlit run enhanced_web_app.py
```

### Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in dashboard:
   ```toml
   GOOGLE_MAPS_API_KEY = "your_key_here"
   ```
4. Deploy

### Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements_enhanced.txt

ENV GOOGLE_MAPS_API_KEY=""

CMD ["streamlit", "run", "enhanced_web_app.py"]
```

```bash
# Build and run
docker build -t pneumonia-app .
docker run -p 8501:8501 \
  -e GOOGLE_MAPS_API_KEY=your_key \
  pneumonia-app
```

### Heroku

```bash
# 1. Create Procfile
echo "web: streamlit run enhanced_web_app.py" > Procfile

# 2. Deploy
heroku create pneumonia-detection
heroku config:set GOOGLE_MAPS_API_KEY=your_key
git push heroku main
```

---

## 🐛 Troubleshooting

### Issue: No hospitals found

**Symptoms**: API returns empty list

**Solutions**:

1. Increase search radius:

   ```python
   hospitals = service.find_nearby_hospitals(
       lat, lon,
       radius=10000  # Try 10km instead of 5km
   )
   ```

2. Check coordinates are valid:

   ```python
   print(f"Searching at: {lat}, {lon}")
   # Should be reasonable values (e.g., 40.7128, -74.0060)
   ```

3. Try different location:

   ```python
   # Try a major city
   coords = service.geocode_address("New York, NY")
   ```

4. Check internet connection

### Issue: Geocoding fails

**Symptoms**: `geocode_address()` returns `None`

**Solutions**:

1. Use more specific address:

   ```python
   # Instead of: "Main Street"
   # Use: "123 Main Street, New York, NY 10001"
   ```

2. Try coordinates directly:

   ```python
   # Skip geocoding, use coordinates
   hospitals = service.find_nearby_hospitals(40.7128, -74.0060)
   ```

3. Check API key (if using Google):
   ```python
   from config.api_config import APIConfig
   print(APIConfig.GOOGLE_MAPS_API_KEY)
   ```

### Issue: Rate limit exceeded

**Symptoms**: "429 Too Many Requests" error

**Solutions**:

1. Add delays between requests:

   ```python
   import time
   for address in addresses:
       coords = service.geocode_address(address)
       time.sleep(1)  # Wait 1 second
   ```

2. Implement caching:

   ```python
   @st.cache_data
   def get_hospitals(lat, lon):
       return service.find_nearby_hospitals(lat, lon)
   ```

3. Upgrade to Google Maps API (higher limits)

### Issue: API key not working

**Symptoms**: "Invalid API key" error

**Solutions**:

1. Verify key is correct:

   ```bash
   # Check .env file
   cat .env
   ```

2. Check API is enabled in Google Cloud Console:

   - Geocoding API ✓
   - Places API ✓

3. Check API restrictions:

   - Remove IP restrictions for testing
   - Check HTTP referrer restrictions

4. Wait for propagation (5-10 minutes after creating key)

### Issue: Map not displaying

**Symptoms**: Blank map or error

**Solutions**:

1. Check Folium is installed:

   ```bash
   pip install folium streamlit-folium
   ```

2. Check coordinates are valid:

   ```python
   print(f"Map center: {user_location}")
   # Should be [latitude, longitude]
   ```

3. Clear Streamlit cache:
   ```bash
   streamlit cache clear
   ```

---

## 📊 Performance

### Response Times

| Operation       | Free API | Google API |
| --------------- | -------- | ---------- |
| Geocoding       | 0.5-2s   | 0.2-0.5s   |
| Hospital Search | 1-3s     | 0.3-1s     |
| Total           | 1.5-5s   | 0.5-1.5s   |

### Optimization Tips

1. **Cache Results**:

   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def get_hospitals(lat, lon):
       return service.find_nearby_hospitals(lat, lon)
   ```

2. **Reduce Search Radius**:

   ```python
   # Smaller radius = faster search
   hospitals = service.find_nearby_hospitals(
       lat, lon,
       radius=3000  # 3km instead of 5km
   )
   ```

3. **Limit Results**:
   ```python
   # Fewer results = faster response
   hospitals = service.find_nearby_hospitals(
       lat, lon,
       max_results=5  # Instead of 10
   )
   ```

---

## 📚 Additional Resources

### Documentation

- [MAP_API_SETUP_GUIDE.md](MAP_API_SETUP_GUIDE.md) - Complete setup guide
- [LOCATION_API_QUICK_START.md](LOCATION_API_QUICK_START.md) - Quick reference
- [examples/location_api_examples.py](examples/location_api_examples.py) - Code examples

### External Links

- [Google Maps Platform](https://developers.google.com/maps)
- [OpenStreetMap](https://www.openstreetmap.org)
- [Nominatim API](https://nominatim.org/release-docs/latest/api/Overview/)
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
- [Folium Documentation](https://python-visualization.github.io/folium/)

### Support

- GitHub Issues: [Your repo]/issues
- Stack Overflow: Tag `openstreetmap` or `google-maps-api`
- Google Maps Support: https://developers.google.com/maps/support

---

## ✅ Checklist

### Setup

- [ ] Install requirements: `pip install -r requirements_enhanced.txt`
- [ ] (Optional) Get Google Maps API key
- [ ] (Optional) Create `.env` file with API key
- [ ] Run test: `python test_location_api.py`
- [ ] Verify tests pass

### Testing

- [ ] Test geocoding with your address
- [ ] Test hospital search in your area
- [ ] Test in web app
- [ ] Verify map displays correctly
- [ ] Check hospital information is accurate

### Deployment

- [ ] Add `.env` to `.gitignore`
- [ ] Set environment variables in deployment platform
- [ ] Test in production environment
- [ ] Monitor API usage
- [ ] Set up error logging

---

## 🎉 Conclusion

You now have a fully functional hospital location feature that:

- ✅ Works immediately with no setup
- ✅ Can be upgraded to premium APIs
- ✅ Provides real value to users
- ✅ Is well-tested and documented
- ✅ Integrates seamlessly with your AI system

**Your Pneumonia Detection app is now a complete healthcare solution!**

Users can:

1. Upload X-ray → Get AI diagnosis
2. See treatment recommendations
3. Watch educational videos
4. **Find nearby hospitals** ← NEW!
5. Get contact information
6. Make informed decisions

---

**Questions?** Check the troubleshooting section or see [MAP_API_SETUP_GUIDE.md](MAP_API_SETUP_GUIDE.md)

**Ready to test?**

```bash
streamlit run enhanced_web_app.py
```
