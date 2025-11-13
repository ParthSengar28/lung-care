# 🗺️ Map Location API Setup Guide

This guide will help you integrate real map location APIs into your Pneumonia Detection application to find nearby hospitals.

## 📋 Overview

The application now supports **two modes** for finding nearby hospitals:

1. **Free Mode (No API Key Required)** - Uses OpenStreetMap APIs

   - Nominatim for geocoding
   - Overpass API for finding hospitals
   - No cost, no registration needed
   - Rate-limited but sufficient for most use cases

2. **Premium Mode (Google Maps API)** - More accurate and feature-rich
   - Google Geocoding API
   - Google Places API
   - Requires API key and billing account
   - Better data quality and more features

## 🆓 Option 1: Free Setup (OpenStreetMap - Recommended for Testing)

**No configuration needed!** The app works out of the box with free APIs.

### Features:

- ✅ Geocoding (address to coordinates)
- ✅ Find nearby hospitals
- ✅ Distance calculation
- ✅ Basic hospital information
- ⚠️ Rate limited (1 request per second for Nominatim)

### Usage:

Just run the app - it will automatically use free APIs if no Google API key is configured.

---

## 🌟 Option 2: Google Maps API Setup (Recommended for Production)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `pneumonia-detection-app`
4. Click "Create"

### Step 2: Enable Required APIs

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API**
   - **Geocoding API**

### Step 3: Create API Key

1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **API key**
3. Copy your API key (looks like: `AIzaSyD...`)
4. Click **Edit API key** to restrict it:
   - **Application restrictions**:
     - For development: None
     - For production: HTTP referrers (add your domain)
   - **API restrictions**:
     - Select "Restrict key"
     - Choose: Places API, Geocoding API, Maps JavaScript API

### Step 4: Set Up Billing (Required for Google Maps)

1. Go to **Billing** in Google Cloud Console
2. Link a billing account
3. **Don't worry**: Google provides $200 free credit per month
4. Typical usage for this app: ~$5-10/month

### Step 5: Configure Your Application

#### Method A: Using Environment Variables (Recommended)

1. Create a `.env` file in your project root:

```bash
# .env file
GOOGLE_MAPS_API_KEY=AIzaSyD_your_actual_api_key_here
```

2. Add `.env` to your `.gitignore`:

```bash
echo ".env" >> .gitignore
```

#### Method B: Direct Configuration

Edit `config/api_config.py`:

```python
GOOGLE_MAPS_API_KEY = 'AIzaSyD_your_actual_api_key_here'
```

⚠️ **Security Warning**: Never commit API keys to Git!

---

## 🚀 Testing Your Setup

### Test 1: Check API Configuration

```python
from config.api_config import APIConfig

print(f"Google Maps configured: {APIConfig.is_google_maps_configured()}")
print(f"API Key: {APIConfig.GOOGLE_MAPS_API_KEY[:10]}...")
```

### Test 2: Test Geocoding

```python
from src.utils.location_service import LocationService
from config.api_config import APIConfig

service = LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)

# Test geocoding
coords = service.geocode_address("New York, NY")
print(f"Coordinates: {coords}")
```

### Test 3: Test Hospital Search

```python
# Find hospitals near coordinates
hospitals = service.find_nearby_hospitals(40.7128, -74.0060, radius=5000)

for hospital in hospitals:
    print(f"{hospital['name']} - {hospital['distance']} km away")
```

### Test 4: Run the Web App

```bash
streamlit run enhanced_web_app.py
```

Navigate to the "Find Care" tab and enter a location to see nearby hospitals.

---

## 📊 API Usage & Costs

### Free Tier (OpenStreetMap)

- **Cost**: $0
- **Limits**:
  - Nominatim: 1 request/second
  - Overpass: Fair use policy
- **Best for**: Development, testing, low-traffic apps

### Google Maps API Pricing

- **Free Credit**: $200/month
- **Geocoding**: $5 per 1,000 requests
- **Places Nearby Search**: $32 per 1,000 requests
- **Typical monthly cost for this app**: $5-20 (well within free tier)

**Example calculation:**

- 100 users/day × 30 days = 3,000 searches/month
- Cost: 3 × $32 = $96 (still within $200 free credit)

---

## 🔧 Configuration Options

Edit `config/api_config.py` to customize:

```python
class APIConfig:
    # Search radius in meters (default: 5km)
    PLACES_SEARCH_RADIUS = 5000

    # Maximum number of results (default: 10)
    MAX_RESULTS = 10

    # API Keys
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_KEY_HERE')
```

---

## 🐛 Troubleshooting

### Issue: "No hospitals found"

**Solutions:**

1. Check your internet connection
2. Verify API key is correct
3. Ensure APIs are enabled in Google Cloud Console
4. Check if billing is set up (for Google Maps)
5. Try increasing search radius in config

### Issue: "Geocoding failed"

**Solutions:**

1. Try a more specific address (include city, state)
2. Check API key permissions
3. Verify Geocoding API is enabled
4. Try the free Nominatim option

### Issue: "API key not valid"

**Solutions:**

1. Verify API key is copied correctly (no extra spaces)
2. Check API restrictions in Google Cloud Console
3. Ensure required APIs are enabled
4. Wait a few minutes after creating key (propagation delay)

### Issue: Rate limit exceeded

**Solutions:**

1. For Nominatim: Add delays between requests
2. For Google: Check your quota in Cloud Console
3. Implement caching for repeated searches

---

## 🔒 Security Best Practices

### 1. Never Commit API Keys

```bash
# Add to .gitignore
.env
config/api_config.py  # if you hardcode keys
```

### 2. Use Environment Variables

```python
import os
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
```

### 3. Restrict API Keys

- Set HTTP referrer restrictions
- Limit to specific APIs
- Monitor usage in Google Cloud Console

### 4. Rotate Keys Regularly

- Generate new keys every 90 days
- Revoke old keys after migration

---

## 📱 Features Available

### Current Features:

- ✅ Geocode user address to coordinates
- ✅ Find nearby hospitals (5km radius)
- ✅ Display hospitals on interactive map
- ✅ Show distance to each hospital
- ✅ Display hospital ratings (Google API)
- ✅ Show emergency services availability
- ✅ Provide contact information

### Potential Enhancements:

- 🔄 Real-time traffic to hospitals
- 🔄 Hospital wait times
- 🔄 Directions/navigation
- 🔄 Hospital reviews
- 🔄 Ambulance services
- 🔄 Pharmacy locations

---

## 🌐 Alternative APIs

If you want to try other services:

### 1. Mapbox

- Similar to Google Maps
- $0.50 per 1,000 requests
- Good alternative

### 2. HERE Maps

- Enterprise-focused
- Competitive pricing
- Good for high-volume

### 3. OpenCage Geocoding

- Geocoding only
- 2,500 free requests/day
- Simple to use

---

## 📞 Support

### Resources:

- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [OpenStreetMap Nominatim](https://nominatim.org/)
- [Overpass API](https://overpass-api.de/)

### Need Help?

1. Check the troubleshooting section above
2. Review API documentation
3. Check Google Cloud Console for errors
4. Verify billing and quotas

---

## ✅ Quick Start Checklist

- [ ] Decide: Free (OpenStreetMap) or Premium (Google Maps)
- [ ] If Google Maps:
  - [ ] Create Google Cloud project
  - [ ] Enable required APIs
  - [ ] Create API key
  - [ ] Set up billing
  - [ ] Configure API key in app
- [ ] Test geocoding functionality
- [ ] Test hospital search
- [ ] Run the web application
- [ ] Verify map displays correctly
- [ ] Test with different locations

---

## 🎉 You're All Set!

Your Pneumonia Detection app now has real-time hospital location features! Users can:

1. Enter their location
2. See nearby hospitals on a map
3. Get directions and contact information
4. Make informed decisions about seeking care

**Remember**: The app works immediately with free APIs, and you can upgrade to Google Maps later for better features!
