import streamlit as st
import pandas as pd
from pathlib import Path

current_dir = Path(__file__).parent
file_path = current_dir / ".." / ".." / "Data" / "raw" / "airbnb_processed.csv"

data = pd.read_csv(file_path.resolve())
st.write(data)