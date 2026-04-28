import streamlit as st
import folium
import requests
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from geopy.geocoders import ArcGIS

st.title("Enter your listing information")

if 'lat' not in st.session_state:
    st.session_state.lat = 30.0444
if 'lon' not in st.session_state:
    st.session_state.lon = 31.2357

def get_ip_location():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=3)
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon']
    except:
        pass
    return 30.0444, 31.2357

loc = get_geolocation()
if loc and 'coords' in loc:
    if 'gps_synced' not in st.session_state:
        st.session_state.lat = loc['coords']['latitude']
        st.session_state.lon = loc['coords']['longitude']
        st.session_state.gps_synced = True

st.subheader("Find a Specific Location")
st.markdown("You can search by neighborhood or full street address (e.g., *Talaat Harb Street, Downtown Cairo*).")

geolocator = ArcGIS()
with st.form("location_search"):
    col1, col2 = st.columns([4, 1])
    with col1:
        address = st.text_input(
            "Address", 
            placeholder="e.g. 9 Mostafa El Nahas, Nasr City", 
            label_visibility="collapsed"
        )
    with col2:
        submit_search = st.form_submit_button("Search", use_container_width=True)

if submit_search and address:
    with st.spinner("Searching for location..."):
        location = geolocator.geocode(address, timeout=10)

        if not location and "," in address:
            broader_search = address.split(",", 1)[1].strip()
            st.info(f"Exact street not found. Trying broader area: {broader_search}...")
            location = geolocator.geocode(broader_search, timeout=10)
        
    if location:
        st.session_state.lat = location.latitude
        st.session_state.lon = location.longitude
        
        st.success(f"Found: {location.address}")
    else:
        st.warning("We couldn't find that exact location. Try checking the spelling or using a broader area (like just the neighborhood).")

@st.fragment
def render_interactive_map():
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=14)

    folium.Marker(
        [st.session_state.lat, st.session_state.lon], 
        popup="Listing Location", 
        icon=folium.Icon(color="red", icon="home")
    ).add_to(m)

    map_data = st_folium(m, width=700, height=500, key="listing_map")

    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        
        if clicked_lat != st.session_state.lat:
            st.session_state.lat = clicked_lat
            st.session_state.lon = clicked_lon
            st.rerun()

render_interactive_map()
st.success(f"Current Selection: {st.session_state.lat:.4f}, {st.session_state.lon:.4f}")