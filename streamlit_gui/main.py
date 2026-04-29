import streamlit as st
from utils.style_utils import apply_custom_style
from utils.data_loader import get_uncleaned_data

st.set_page_config(page_title="Airbnb Analytics", layout="wide")

home_page = st.Page("pages/0_home.py", title="Dashboard", icon=":material/home:", default=True)
predictor_page = st.Page("pages/1_predictor.py", title="Find your rental's value", icon=":material/dashboard:")

pg = st.navigation([home_page, predictor_page])

apply_custom_style()

pg.run()