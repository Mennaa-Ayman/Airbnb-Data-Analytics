import streamlit as st
import streamlit.components.v1 as components

from utils.data_loader import get_cleaned_data, get_cleaned_reviews, get_heatmap, get_plot_image

st.set_page_config(page_title="Data Analytics", page_icon=":material/analytics:", layout="wide")

st.title("Cairo Airbnb Analytics Dashboard")

st.header("Data Overview")
st.markdown("This is the cleaned Airbnb rentals dataset.")

try:
    df = get_cleaned_data()
    avg_price = df['price_breakdown_baseprice_price'].mean()
    avg_rating = df['rating_overall'].mean()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Average Price", f"EGP {avg_price:,.2f}")
    col4.metric("Average Rating", f"{avg_rating:.2f}")

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

def display_plot(filename):
    img = get_plot_image(filename)
    if img:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image(img, width="stretch")
    else:
        st.error(f"Image `{filename}` not found.")


st.header("Key Insights & Plots")
st.markdown("Select a tab below to view different insights of the data.")

plot_files = {
    "Price Distribution": "price_distribution.png",
    "Rating vs Price": "price_vs_ratings.png",
    "Reviews Overview": "reviews_distribution.png",
    "Review Count vs Price": "price_vs_reviews.png",
    "Price by Amenity": "price_by_amenity.png",
    "Price vs Bedrooms": "price_vs_bedrooms.png",
    "Rating by Amenity": "rating_by_amenity.png",
    "Top 10 Reviews": "top10_reviews.png",
    "Price by Sentiment": "sentiment_price.png"
}

tabs = st.tabs(list(plot_files.keys()))

for tab, (title, filename) in zip(tabs, plot_files.items()):
    with tab:
        display_plot(filename)