import streamlit as st
from utils.data_loader import get_uncleaned_data

st.title("My Dashboard")
st.write("Hello, Welcome to the Airbnb Data Analytics App!")

st.write("The collected data (uncleaned version) is stored in a CSV file. Below is a preview of the data:")

data = get_uncleaned_data()

col1, col2 = st.columns(2)
col1.metric("Total Rows", data.shape[0])
col2.metric("Total Columns", data.shape[1])

st.dataframe(data, width="stretch")