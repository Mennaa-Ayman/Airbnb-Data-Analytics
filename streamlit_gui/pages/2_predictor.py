import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from geopy.geocoders import ArcGIS
from utils.data_loader import get_prediction_model

st.set_page_config(page_title="Price Predictor", page_icon=":material/dashboard:", layout="wide")

st.title("Enter your listing information")

def inline_number_input(label, min_val=0, step=1):
    label_col, input_col = st.columns([1, 2]) 
    
    with label_col:
        st.markdown(f"<div style='margin-top: 10px;'><b>{label}</b></div>", unsafe_allow_html=True)
        
    with input_col:
        return st.number_input(
            label, 
            min_value=min_val, 
            step=step, 
            label_visibility="collapsed"
        )
    
def inline_selectbox(label, options):
    label_col, input_col = st.columns([1, 2])
    with label_col:
        st.markdown(f"<div style='margin-top: 10px;'><b>{label}</b></div>", unsafe_allow_html=True)
    with input_col:
        return st.selectbox(label, options=options, label_visibility="collapsed")
    
st.subheader("Property Details")
bedrooms = inline_number_input("Number of bedrooms", min_val=0, step=1)
bathrooms = inline_number_input("Number of bathrooms", min_val=0, step=1)

st.subheader("Amenities & Views")
col1, col2, col3 = st.columns(3)
with col1:
    has_wifi = st.checkbox("WiFi")
with col2:
    has_pool = st.checkbox("Pool")
with col3:
    has_pyramid_view = st.checkbox("Pyramid View")

st.subheader("Description")
description = st.text_area("Write your listing description here:", height=100)
description_length = len(description)
st.caption(f"**Calculated Description Length:** {description_length} characters")

st.divider()

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

st.divider()
st.subheader("Price Prediction")
st.markdown("Ready to see how much this listing could make?")

if "predicted_price" not in st.session_state:
    st.session_state.predicted_price = None

if st.button("Predict Price", type="primary", use_container_width=True):
    price_predictor, expected_features = get_prediction_model()

    raw_inputs = {
        "lat": st.session_state.lat,
        "lng": st.session_state.lon,
        "rating_overall": 0, 
        "reviews_count": 0,   
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "description_length": description_length,
        "has_wifi": bool(has_wifi),
        "has_pool": bool(has_pool)
    }
    
    with st.spinner("Calculating optimal price..."):
        input_df = pd.DataFrame([raw_inputs], columns=expected_features)
        prediction = price_predictor.predict(input_df)[0]
        st.session_state.predicted_price = float(prediction)
        
if st.session_state.predicted_price is not None:
    st.success("Prediction Complete!")
    st.metric(label="Suggested Nightly Price", value=f"EGP {st.session_state.predicted_price:,.2f}")
    
    if st.button("Clear Prediction"):
        st.session_state.predicted_price = None
        st.rerun()
