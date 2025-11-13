"""
Test script for Location API functionality
Run this to verify your API setup is working correctly
"""
import sys
sys.path.append('.')

from src.utils.location_service import LocationService
from config.api_config import APIConfig

def test_api_configuration():
    """Test API configuration"""
    print("=" * 60)
    print("🔧 API Configuration Test")
    print("=" * 60)
    
    print(f"\n✓ Google Maps API configured: {APIConfig.is_google_maps_configured()}")
    
    if APIConfig.is_google_maps_configured():
        print(f"✓ API Key: {APIConfig.GOOGLE_MAPS_API_KEY[:20]}...")
    else:
        print("ℹ️  No Google Maps API key - will use free OpenStreetMap APIs")
    
    print(f"✓ Search radius: {APIConfig.PLACES_SEARCH_RADIUS} meters")
    print(f"✓ Max results: {APIConfig.MAX_RESULTS}")

def test_geocoding():
    """Test geocoding functionality"""
    print("\n" + "=" * 60)
    print("📍 Geocoding Test")
    print("=" * 60)
    
    service = LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)
    
    test_addresses = [
        "New York, NY",
        "Los Angeles, CA",
        "Chicago, IL"
    ]
    
    for address in test_addresses:
        print(f"\n🔍 Testing: {address}")
        coords = service.geocode_address(address)
        
        if coords:
            print(f"   ✅ Success: {coords[0]:.4f}, {coords[1]:.4f}")
        else:
            print(f"   ❌ Failed to geocode")

def test_hospital_search():
    """Test hospital search functionality"""
    print("\n" + "=" * 60)
    print("🏥 Hospital Search Test")
    print("=" * 60)
    
    service = LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)
    
    # Test location: New York City
    test_lat, test_lon = 40.7128, -74.0060
    
    print(f"\n🔍 Searching for hospitals near: {test_lat}, {test_lon}")
    print(f"   Radius: {APIConfig.PLACES_SEARCH_RADIUS}m")
    
    hospitals = service.find_nearby_hospitals(
        test_lat, 
        test_lon,
        radius=APIConfig.PLACES_SEARCH_RADIUS,
        max_results=5
    )
    
    if hospitals:
        print(f"\n✅ Found {len(hospitals)} hospitals:")
        for i, hospital in enumerate(hospitals, 1):
            print(f"\n   {i}. {hospital['name']}")
            print(f"      📍 Address: {hospital['address']}")
            print(f"      📏 Distance: {hospital['distance']} km")
            if 'phone' in hospital:
                print(f"      📞 Phone: {hospital['phone']}")
            if 'rating' in hospital and hospital['rating']:
                print(f"      ⭐ Rating: {hospital['rating']}")
    else:
        print("\n❌ No hospitals found")
        print("   Possible reasons:")
        print("   - API key not configured correctly")
        print("   - Network connection issues")
        print("   - No hospitals in search radius")

def test_distance_calculation():
    """Test distance calculation"""
    print("\n" + "=" * 60)
    print("📏 Distance Calculation Test")
    print("=" * 60)
    
    service = LocationService()
    
    # New York to Los Angeles
    ny_coords = (40.7128, -74.0060)
    la_coords = (34.0522, -118.2437)
    
    distance = service._calculate_distance(
        ny_coords[0], ny_coords[1],
        la_coords[0], la_coords[1]
    )
    
    print(f"\n📍 New York: {ny_coords}")
    print(f"📍 Los Angeles: {la_coords}")
    print(f"📏 Distance: {distance} km")
    print(f"   (Expected: ~3,944 km)")
    
    if 3900 < distance < 4000:
        print("   ✅ Distance calculation accurate!")
    else:
        print("   ⚠️  Distance calculation may have issues")

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 Location API Test Suite")
    print("=" * 60)
    
    try:
        test_api_configuration()
        test_geocoding()
        test_hospital_search()
        test_distance_calculation()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
        if not APIConfig.is_google_maps_configured():
            print("\n💡 Tip: Configure Google Maps API for better results")
            print("   See MAP_API_SETUP_GUIDE.md for instructions")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
