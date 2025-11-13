# 🚀 Location API Quick Start

Get your map location feature working in 5 minutes!

## ⚡ Fastest Way (No API Key Required)

The app works **immediately** with free OpenStreetMap APIs:

```bash
# 1. Install dependencies
pip install -r requirements_enhanced.txt

# 2. Run the app
streamlit run enhanced_web_app.py

# 3. Go to "Find Care" tab and enter a location
# That's it! 🎉
```

## 🔧 How It Works

### Without API Key (Free Mode)

- Uses **Nominatim** for geocoding (address → coordinates)
- Uses **Overpass API** for finding hospitals
- **No registration needed**
- Works worldwide
- Rate limited but sufficient for testing

### With Google Maps API (Premium Mode)

- More accurate results
- Better hospital data
- Ratings and reviews
- Real-time information
- See `MAP_API_SETUP_GUIDE.md` for setup

## 📝 Basic Usage

### 1. In Python Script

```python
from src.utils.location_service import LocationService

# Initialize (works without API key)
service = LocationService()

# Find hospitals near coordinates
hospitals = service.find_nearby_hospitals(
    latitude=40.7128,
    longitude=-74.0060,
    radius=5000,  # 5km
    max_results=10
)

for hospital in hospitals:
    print(f"{hospital['name']} - {hospital['distance']} km")
```

### 2. In Streamlit App

```python
import streamlit as st
from src.utils.location_service import LocationService

service = LocationService()

# Get user location
address = st.text_input("Enter your location")

if address:
    coords = service.geocode_address(address)
    if coords:
        hospitals = service.find_nearby_hospitals(coords[0], coords[1])
        st.write(f"Found {len(hospitals)} hospitals")
```

## 🧪 Test Your Setup

```bash
# Run the test script
python test_location_api.py
```

Expected output:

```
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
```

## 🎯 Common Use Cases

### Find Closest Hospital

```python
hospitals = service.find_nearby_hospitals(lat, lon, max_results=1)
closest = hospitals[0]
print(f"Closest: {closest['name']} - {closest['distance']} km")
```

### Find Emergency Hospitals

```python
hospitals = service.find_nearby_hospitals(lat, lon, radius=10000)
emergency = [h for h in hospitals if h.get('emergency', True)]
```

### Get Hospital by Address

```python
# Step 1: Geocode
coords = service.geocode_address("123 Main St, New York, NY")

# Step 2: Search
if coords:
    hospitals = service.find_nearby_hospitals(coords[0], coords[1])
```

## 🔑 Add Google Maps API (Optional)

1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create `.env` file:
   ```bash
   GOOGLE_MAPS_API_KEY=AIzaSyD_your_key_here
   ```
3. Restart the app

See `MAP_API_SETUP_GUIDE.md` for detailed instructions.

## 📊 API Comparison

| Feature         | Free (OSM) | Google Maps            |
| --------------- | ---------- | ---------------------- |
| Cost            | $0         | $200/month free credit |
| Setup           | None       | API key required       |
| Geocoding       | ✅ Good    | ✅ Excellent           |
| Hospital Search | ✅ Good    | ✅ Excellent           |
| Ratings         | ❌ No      | ✅ Yes                 |
| Reviews         | ❌ No      | ✅ Yes                 |
| Real-time Data  | ❌ No      | ✅ Yes                 |
| Rate Limits     | 1 req/sec  | 1000s req/sec          |

## 🐛 Troubleshooting

### "No hospitals found"

- Try increasing search radius
- Check internet connection
- Try a different location

### "Geocoding failed"

- Use more specific address
- Include city and state
- Try coordinates directly

### "Rate limit exceeded"

- Wait a few seconds between requests
- Consider Google Maps API for higher limits

## 📚 More Resources

- **Full Setup Guide**: `MAP_API_SETUP_GUIDE.md`
- **Code Examples**: `examples/location_api_examples.py`
- **Test Script**: `test_location_api.py`
- **API Config**: `config/api_config.py`

## ✅ Quick Checklist

- [ ] Install requirements: `pip install -r requirements_enhanced.txt`
- [ ] Run test: `python test_location_api.py`
- [ ] Run app: `streamlit run enhanced_web_app.py`
- [ ] Test "Find Care" tab
- [ ] (Optional) Add Google Maps API key

## 🎉 You're Ready!

Your app now has real-time hospital location features with **zero configuration**!

For production use, consider adding a Google Maps API key for better results.
