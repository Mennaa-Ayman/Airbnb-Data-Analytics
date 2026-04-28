import streamlit as st
import pandas as pd

from pathlib import Path

@st.cache_data
def get_uncleaned_data():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Data" / "raw" / "airbnb_processed.csv"
    return pd.read_csv(file_path.resolve())