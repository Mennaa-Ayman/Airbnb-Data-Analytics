import streamlit as st
import pandas as pd
import folium
from datetime import date, timedelta
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from geopy.geocoders import ArcGIS
from utils.data_loader import get_prediction_model

st.set_page_config(page_title="Price Predictor", page_icon=":material/dashboard:", layout="wide")

st.title("Enter your listing information")

def inline_number_input(label, min_val=0, step=1, value=0):
    label_col, input_col = st.columns([1, 2])
    with label_col:
        st.markdown(f"<div style='margin-top: 10px;'><b>{label}</b></div>", unsafe_allow_html=True)
    with input_col:
        return st.number_input(
            label,
            min_value=float(min_val),
            step=float(step),
            value=float(value),
            label_visibility="collapsed"
        )

# ── Property Details ─────────────────────────────────────────────────
st.subheader("Property Details")
bedrooms  = inline_number_input("Number of bedrooms",  min_val=0, step=1)
# bathrooms = inline_number_input("Number of bathrooms", min_val=0, step=0.5)

# Show bathroom input per bedroom dynamically
total_bathrooms = 0
if bedrooms > 0:
    st.write("**Bathrooms per bedroom:**")
    for i in range(int(bedrooms)):
        baths = inline_number_input(f"Bedroom {i+1} bathrooms", min_val=0, step=0.5)
        total_bathrooms += baths
else:
    total_bathrooms = inline_number_input("Number of bathrooms", min_val=0, step=0.5)

st.write(f"Total bathrooms: **{total_bathrooms}**")

# ── Ratings & Reviews ────────────────────────────────────────────────
st.subheader("Ratings & Reviews")
col_r1, col_r2 = st.columns(2)
with col_r1:
    rating_overall = st.slider(
        "Overall rating",
        min_value=0.0, max_value=5.0, value=4.5, step=0.01,
        help="Average guest rating (0 = no rating yet)"
    )
with col_r2:
    reviews_count = st.number_input(
        "Number of reviews",
        min_value=0, step=1, value=0,
        help="Total number of guest reviews"
    )

# ── Stay Dates ───────────────────────────────────────────────────────
st.subheader("Stay Dates")
today = date.today()
col_d1, col_d2 = st.columns(2)
with col_d1:
    checkin_date = st.date_input("Check-in date", value=today, min_value=today)
with col_d2:
    checkout_date = st.date_input(
        "Check-out date",
        value=today + timedelta(days=1),
        min_value=checkin_date + timedelta(days=1)
    )

# ── Amenities & Views ────────────────────────────────────────────────
st.subheader("Amenities & Views")
col1, col2, col3 = st.columns(3)
with col1:
    has_wifi         = st.checkbox("WiFi")
with col2:
    has_pool         = st.checkbox("Pool")

st.divider()

# ── Location ─────────────────────────────────────────────────────────
if 'lat' not in st.session_state:
    st.session_state.lat = 30.0444
if 'lon' not in st.session_state:
    st.session_state.lon = 31.2357

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
        st.warning("We couldn't find that exact location. Try checking the spelling or using a broader area.")

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

# ── Price Prediction ─────────────────────────────────────────────────
st.subheader("Price Prediction")
st.markdown("Ready to see how much this listing could make?")

if "predicted_price" not in st.session_state:
    st.session_state.predicted_price = None

if st.button("Predict Price", type="primary", use_container_width=True):
    price_predictor, expected_features = get_prediction_model()
    inputs = {
        "lat":                st.session_state.lat,
        "lng":                st.session_state.lon,
        "rating_overall":     rating_overall,
        "reviews_count":      reviews_count,
        "checkin_year":       checkin_date.year,
        "checkin_month":      checkin_date.month,
        "checkin_day":        checkin_date.day,
        "checkin_weekday":    checkin_date.weekday(),
        "checkout_year":      checkout_date.year,
        "checkout_month":     checkout_date.month,
        "checkout_day":       checkout_date.day,
        "checkout_weekday":   checkout_date.weekday(),
        "bedrooms":           bedrooms,
        "bathrooms":          total_bathrooms,
        "description_length": 0,
        "has_wifi":           bool(has_wifi),
        "has_pool":           bool(has_pool)
        }
    with st.spinner("Calculating optimal price..."):
        input_df = pd.DataFrame([inputs], columns=expected_features)
        prediction = price_predictor.predict(input_df)[0]
        st.session_state.predicted_price = float(prediction)

if st.session_state.predicted_price is not None:
    st.success("Prediction Complete!")
    st.metric(label="Suggested Price", value=f"$ {st.session_state.predicted_price:,.2f}")
    if st.button("Clear Prediction"):
        st.session_state.predicted_price = None
        st.rerun()