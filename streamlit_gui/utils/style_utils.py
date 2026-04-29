import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .main { background-color: #f5f5f5; }
        h1 { color: #ff5a5f; }
        </style>
        """, unsafe_allow_html=True)