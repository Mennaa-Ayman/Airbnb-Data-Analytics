import streamlit as st
import pandas as pd
import joblib
import json

from pathlib import Path
from PIL import Image

@st.cache_data
def get_uncleaned_data():
    current_dir = Path(__file__).parent
    file_path = current_dir / ".." / ".." / "Data" / "raw" / "Uncleaned_data.csv"
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
    

@st.cache_resource
def get_prediction_model():
    current_dir = Path(__file__).parent
    model_path = current_dir / ".." / ".." / "Models" / "Models" / "random_forest.pkl"
    features_path = current_dir / ".." / ".." / "Models" / "Models" / "feature_columns.json"
    
    model = joblib.load(model_path.resolve())
    with open(features_path.resolve(), 'r') as f:
        features = json.load(f)
        
    return model, features