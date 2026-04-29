import streamlit as st
import pandas as pd

from pathlib import Path
from PIL import Image

@st.cache_data
def get_uncleaned_data():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Data" / "raw" / "airbnb_processed.csv"
    return pd.read_csv(file_path.resolve())


@st.cache_data
def get_uncleaned_reviews():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Data" / "raw" / "rentals_reviews.csv"
    return pd.read_csv(file_path.resolve())



@st.cache_data
def get_cleaned_data():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Data" / "clean" / "airbnb_cleaned.csv"
    return pd.read_csv(file_path.resolve())

@st.cache_data
def get_cleaned_reviews():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Data" / "clean" / "rentals_reviews_with_sentiment.csv"
    return pd.read_csv(file_path.resolve())


@st.cache_data
def get_heatmap():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Plots" / "cairo_heatmap.html"
    with open(file_path.resolve(), "r", encoding="utf-8") as f:
        return f.read()
    

@st.cache_data
def get_plot_image(filename):
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Plots" / filename
    
    try:
        return Image.open(file_path.resolve())
    except FileNotFoundError:
        return None