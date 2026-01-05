"""
Property Investment Insights: Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.data_processing import DataProcessor
from utils.visualizations import Visualizer

# Page configuration
st.set_page_config(
    page_title="Property Investment Insights",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🏠 Property Investment Insights Dashboard")

# Load data
@st.cache_data
def load_data():
    base_path = Path(__file__).parent
    demographics_path = base_path / "data" / "demographics.csv"
    listings_path = base_path / "data" / "listings.csv"
    
    processor = DataProcessor(str(demographics_path), str(listings_path))
    return processor.process_all_data()

# Main app
df = load_data()
st.success(f"Loaded {len(df)} properties")
st.dataframe(df.head())
