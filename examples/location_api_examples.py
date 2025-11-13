"""
Examples of using the Location API in different scenarios
"""
import sys
sys.path.append('..')

from src.utils.location_service import LocationService
from config.api_config import APIConfig

# Initialize the service
location_service = LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)

# ============================================================================
# Example 1: Find hospitals near a specific address
# ============================================================================
def example_1_address_search():
    """Find hospitals near a user's address"""
    print("\n" + "="*60)
    print("Example 1: Find Hospitals Near Address")
    print("="*60)
    
    # User enters their address
    user_address = "1600 Amphitheatre Parkway, Mountain View, CA"
    
    # Step 1: Convert address to coordinates
    print(f"\n📍 Geocoding address: {user_address}")
    coords = location_service.geocode_address(user_address)
    
    if coords:
        print(f"✅ Location found: {coords[0]:.4f}, {coords[1]:.4f}")
        
        # Step 2: Find nearby hospitals
        print(f"\n🔍 Searching for hospitals within 5km...")
        hospitals = location_service.find_nearby_hospitals(
            coords[0], coords[1],
            radius=5000,
            max_results=5
        )
        
        # Step 3: Display results
        if hospitals:
            print(f"\n✅ Found {len(hospitals)} hospitals:\n")
            for i, hospital in enumerate(hospitals, 1):
                print(f"{i}. {hospital['name']}")
                print(f"   📍 {hospital['address']}")
                print(f"   📏 {hospital['distance']} km away")
                if hospital.get('phone') != 'N/A':
                    print(f"   📞 {hospital['phone']}")
                print()
        else:
            print("❌ No hospitals found in this area")
    else:
        print("❌ Could not geocode address")

# ============================================================================
# Example 2: Find emergency hospitals only
# ============================================================================
def example_2_emergency_only():
    """Filter for emergency hospitals only"""
    print("\n" + "="*60)
    print("Example 2: Find Emergency Hospitals Only")
    print("="*60)
    
    # Coordinates for downtown Los Angeles
    lat, lon = 34.0522, -118.2437
    
    print(f"\n🔍 Searching for emergency hospitals near LA...")
    hospitals = location_service.find_nearby_hospitals(
        lat, lon,
        radius=10000,  # 10km radius
        max_results=20
    )
    
    # Filter for emergency hospitals
    emergency_hospitals = [h for h in hospitals if h.get('emergency', True)]
    
    print(f"\n✅ Found {len(emergency_hospitals)} emergency hospitals:\n")
    for i, hospital in enumerate(emergency_hospitals[:5], 1):
        print(f"{i}. 🚨 {hospital['name']}")
        print(f"   📏 {hospital['distance']} km away")
        print()

# ============================================================================
# Example 3: Find closest hospital
# ============================================================================
def example_3_closest_hospital():
    """Find the single closest hospital"""
    print("\n" + "="*60)
    print("Example 3: Find Closest Hospital")
    print("="*60)
    
    # User's current location (Chicago)
    lat, lon = 41.8781, -87.6298
    
    print(f"\n🔍 Finding closest hospital to: {lat}, {lon}")
    hospitals = location_service.find_nearby_hospitals(
        lat, lon,
        radius=5000,
        max_results=1  # Only get the closest one
    )
    
    if hospitals:
        closest = hospitals[0]
        print(f"\n✅ Closest hospital:")
        print(f"   🏥 {closest['name']}")
        print(f"   📍 {closest['address']}")
        print(f"   📏 {closest['distance']} km away")
        if closest.get('phone') != 'N/A':
            print(f"   📞 {closest['phone']}")
        
        # Calculate estimated travel time (assuming 40 km/h average speed)
        travel_time = (closest['distance'] / 40) * 60  # minutes
        print(f"   🚗 Estimated travel time: {travel_time:.0f} minutes")

# ============================================================================
# Example 4: Compare multiple locations
# ============================================================================
def example_4_compare_locations():
    """Compare hospital availability in different cities"""
    print("\n" + "="*60)
    print("Example 4: Compare Hospital Availability")
    print("="*60)
    
    cities = {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698)
    }
    
    print("\n🔍 Comparing hospital availability in major cities:\n")
    
    for city, (lat, lon) in cities.items():
        hospitals = location_service.find_nearby_hospitals(
            lat, lon,
            radius=5000,
            max_results=10
        )
        
        if hospitals:
            avg_distance = sum(h['distance'] for h in hospitals) / len(hospitals)
            print(f"{city}:")
            print(f"   🏥 Hospitals found: {len(hospitals)}")
            print(f"   📏 Average distance: {avg_distance:.2f} km")
            print(f"   🏥 Closest: {hospitals[0]['name']} ({hospitals[0]['distance']} km)")
            print()

# ============================================================================
# Example 5: Get detailed hospital information
# ============================================================================
def example_5_hospital_details():
    """Get detailed information about a specific hospital"""
    print("\n" + "="*60)
    print("Example 5: Get Hospital Details")
    print("="*60)
    
    # First, find hospitals
    lat, lon = 40.7128, -74.0060  # New York
    
    print(f"\n🔍 Finding hospitals in New York...")
    hospitals = location_service.find_nearby_hospitals(
        lat, lon,
        radius=3000,
        max_results=3
    )
    
    if hospitals:
        print(f"\n✅ Found {len(hospitals)} hospitals:\n")
        
        for i, hospital in enumerate(hospitals, 1):
            print(f"{i}. {hospital['name']}")
            print(f"   📍 Address: {hospital['address']}")
            print(f"   📏 Distance: {hospital['distance']} km")
            
            # Get rating if available
            if hospital.get('rating'):
                stars = '⭐' * int(hospital['rating'])
                print(f"   {stars} {hospital['rating']}/5")
            
            # Get additional details if place_id is available (Google API only)
            if hospital.get('place_id'):
                details = location_service.get_hospital_details(hospital['place_id'])
                if details:
                    if details.get('website'):
                        print(f"   🌐 Website: {details['website']}")
                    if details.get('formatted_phone_number'):
                        print(f"   📞 Phone: {details['formatted_phone_number']}")
            
            print()

# ============================================================================
# Example 6: Handle errors gracefully
# ============================================================================
def example_6_error_handling():
    """Demonstrate error handling"""
    print("\n" + "="*60)
    print("Example 6: Error Handling")
    print("="*60)
    
    # Test with invalid address
    print("\n🔍 Testing with invalid address...")
    coords = location_service.geocode_address("asdfghjkl12345")
    
    if coords:
        print(f"✅ Coordinates: {coords}")
    else:
        print("❌ Could not geocode address (expected)")
        print("   Fallback: Using default location")
        coords = (40.7128, -74.0060)  # Default to NYC
    
    # Test with remote location (middle of ocean)
    print("\n🔍 Testing with remote location (middle of ocean)...")
    hospitals = location_service.find_nearby_hospitals(
        0.0, 0.0,  # Middle of Atlantic Ocean
        radius=5000,
        max_results=5
    )
    
    if hospitals:
        print(f"✅ Found {len(hospitals)} hospitals")
    else:
        print("❌ No hospitals found (expected)")
        print("   Fallback: Show message to user")

# ============================================================================
# Example 7: Integration with Streamlit app
# ============================================================================
def example_7_streamlit_integration():
    """Example of how to use in Streamlit app"""
    print("\n" + "="*60)
    print("Example 7: Streamlit Integration Pattern")
    print("="*60)
    
    print("""
# In your Streamlit app:

import streamlit as st
from src.utils.location_service import LocationService
from config.api_config import APIConfig

# Initialize service
@st.cache_resource
def get_location_service():
    return LocationService(google_api_key=APIConfig.GOOGLE_MAPS_API_KEY)

service = get_location_service()

# Get user input
user_address = st.text_input("Enter your location")

if user_address:
    # Geocode address
    with st.spinner("Finding your location..."):
        coords = service.geocode_address(user_address)
    
    if coords:
        st.success(f"Location found: {coords}")
        
        # Find hospitals
        with st.spinner("Searching for nearby hospitals..."):
            hospitals = service.find_nearby_hospitals(
                coords[0], coords[1],
                radius=5000,
                max_results=10
            )
        
        if hospitals:
            st.success(f"Found {len(hospitals)} hospitals")
            
            # Display results
            for hospital in hospitals:
                with st.expander(hospital['name']):
                    st.write(f"📍 {hospital['address']}")
                    st.write(f"📏 {hospital['distance']} km away")
                    if hospital.get('phone') != 'N/A':
                        st.write(f"📞 {hospital['phone']}")
        else:
            st.warning("No hospitals found nearby")
    else:
        st.error("Could not find location")
    """)

# ============================================================================
# Run all examples
# ============================================================================
def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("🗺️  Location API Examples")
    print("="*60)
    
    print("\nThese examples demonstrate how to use the Location API")
    print("in your Pneumonia Detection application.\n")
    
    # Check API configuration
    if APIConfig.is_google_maps_configured():
        print("✅ Using Google Maps API")
    else:
        print("ℹ️  Using free OpenStreetMap APIs")
    
    try:
        example_1_address_search()
        example_2_emergency_only()
        example_3_closest_hospital()
        example_4_compare_locations()
        example_5_hospital_details()
        example_6_error_handling()
        example_7_streamlit_integration()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
