import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
import os

from utils.data_loader import get_cleaned_data, get_cleaned_reviews, get_heatmap, get_plot_image

st.title("Cairo Airbnb Analytics Dashboard")

st.header("Data Overview")
st.markdown("This is the cleaned Airbnb rentals dataset.")

try:
    df = get_cleaned_data()
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    st.dataframe(df, width="stretch") 
except FileNotFoundError:
    st.error(f"Could not find the dataset of the rentals. Please check the path.")

st.markdown("This is the cleaned Airbnb reviews dataset.")

try:
    df_reviews = get_cleaned_reviews()
    avg_reviews_per_rental = len(df_reviews) / df_reviews['room_id'].nunique()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df_reviews.shape[0])
    col2.metric("Total Columns", df_reviews.shape[1])
    col3.metric("Avg Collected Reviews per Rental", f"{avg_reviews_per_rental:.2f}")
    st.dataframe(df_reviews, width="stretch") 
except FileNotFoundError:
    st.error(f"Could not find the dataset of the reviews. Please check the path.")

st.divider()

st.header("Cairo Heatmap")

try:
    heatmap_html = get_heatmap()
    components.html(heatmap_html, height=600, scrolling=True)
except FileNotFoundError:
    st.error(f"Could not find the heatmap.")

st.divider()

st.header("Key Insights & Plots")
st.markdown("Select a tab below to view different cuts of the data.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Price Distribution", 
    "Rating vs Price", 
    "Reviews Overview", 
    "Reviews vs Discount", 
    "Review Count vs Price"
])

def display_plot(filename):
    img = get_plot_image(filename)
    if img:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image(img, width="stretch")
    else:
        st.error(f"Image `{filename}` not found.")

with tab1:
    display_plot("Price_Distribution.png")

with tab2:
    display_plot("Rating_Vs_Price.png")

with tab3:
    display_plot("Reviews_chart.png")

with tab4:
    display_plot("Reviews_Vs_discount.png")

with tab5:
    display_plot("reviewsCount_Vs_Price.png")