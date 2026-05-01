import streamlit as st
from utils.data_loader import get_uncleaned_data, get_uncleaned_reviews

st.set_page_config(page_title="Home", page_icon=":material/home:", layout="wide")

st.title("My Dashboard")
st.write("Hello, Welcome to the Airbnb Data Analytics App!")

st.write("The collected rentals data (uncleaned version) is stored in a CSV file. Below is a preview of the data:")

data = get_uncleaned_data()

col1, col2 = st.columns(2)
col1.metric("Total Rows", data.shape[0])
col2.metric("Total Columns", data.shape[1])

st.dataframe(data, width="stretch")


st.write("The collected reviews data (uncleaned version) is stored in a CSV file. Below is a preview of the data:")
reviews = get_uncleaned_reviews()
col1, col2 = st.columns(2)
col1.metric("Total Rows", reviews.shape[0])
col2.metric("Total Columns", reviews.shape[1])
st.dataframe(reviews, width="stretch")