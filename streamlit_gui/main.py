import streamlit as st
from utils.style_utils import apply_custom_style
from utils.data_loader import get_uncleaned_data

st.set_page_config(page_title="Airbnb Analytics", layout="wide")

home_page = st.Page("pages/0_home.py", title="Dashboard", icon=":material/home:", default=True)
analytics_page = st.Page("pages/1_analytics.py", title="Data Analytics", icon=":material/analytics:")
predictor_page = st.Page("pages/2_predictor.py", title="Find your rental's value", icon=":material/dashboard:")
rental_search_page = st.Page("pages/3_rental_search.py", title="Search Rentals", icon=":material/search:")

pg = st.navigation([home_page, analytics_page, predictor_page, rental_search_page])

apply_custom_style()

pg.run()