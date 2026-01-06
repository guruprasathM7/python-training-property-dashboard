"""
Property Investment Insights: Streamlit Dashboard

A comprehensive dashboard for analyzing property investment opportunities
by integrating messy listing data with structured demographic information.

Author: CloudThat - Kantar Python Capstone Project
Date: January 2026
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Import custom modules
from utils.data_processing import DataProcessor
from utils.visualizations import Visualizer


# Page configuration
st.set_page_config(
    page_title="Property Investment Insights",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force sidebar to be visible
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Custom CSS for sleek, modern UI
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Force sidebar to always be visible and prevent collapse */
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        transition: none !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(0) !important;
    }
    
    /* Completely hide collapse button and related controls - all states */
    [data-testid="collapsedControl"],
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] > div > button,
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] header button,
    button[aria-label*="Close"],
    button[aria-label*="collapse"],
    button[data-testid*="collapse"],
    .css-1dp5vir,
    .css-17eq0hr,
    .st-emotion-cache-1dp5vir,
    .st-emotion-cache-17eq0hr,
    [data-testid="stSidebar"] [data-testid="baseButton-header"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-header"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    /* Remove hover effects that might show buttons */
    [data-testid="stSidebar"]:hover button,
    [data-testid="stSidebar"] > div:hover > button {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* Main container with gradient */
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2.5rem 3.5rem;
        max-width: 1440px;
        margin: 0 auto;
    }
    
    /* Metrics - Professional card design */
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: none;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
        font-weight: 500;
        color: rgba(255,255,255,0.65);
        text-transform: none;
        letter-spacing: 0;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        transition: all 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.12);
    }
    
    /* Headers - Professional typography */
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: none;
        letter-spacing: -0.02em !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-left: 0;
        border-left: none;
        text-shadow: none;
    }
    
    h3 {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500 !important;
        font-size: 1.15rem !important;
        margin-top: 1.5rem !important;
    }
    
    /* Sidebar - Professional clean design */
    [data-testid="stSidebar"] {
        background: #1a1f2e;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        min-width: 260px !important;
        max-width: 280px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
        padding: 1rem 0.875rem;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.1rem !important;
        margin-bottom: 0.75rem !important;
        padding: 0;
        background: transparent;
        border-radius: 0;
        text-align: left;
        font-weight: 600;
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #9ca3af !important;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-size: 0.95rem !important;
        margin: 0.5rem 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #d1d5db !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: none;
        letter-spacing: 0;
        margin-bottom: 0.375rem !important;
    }
    
    /* Professional expanders in sidebar - compact */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 6px;
        margin-bottom: 0.625rem;
        padding: 0;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"]:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        font-size: 0.85rem !important;
        padding: 0.625rem 0.875rem !important;
        font-weight: 500;
        color: #e5e7eb;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] > div {
        padding: 0.5rem 0.875rem 0.75rem 0.875rem !important;
    }
    
    /* Compact sliders */
    [data-testid="stSidebar"] .stSlider {
        padding: 0.25rem 0;
        margin-bottom: 0.75rem;
    }
    
    [data-testid="stSidebar"] .stSlider label {
        font-size: 0.8rem !important;
        margin-bottom: 0.375rem !important;
    }
    
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }
    
    /* Compact and professional multiselect */
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stMultiSelect label {
        font-size: 0.8rem !important;
        margin-bottom: 0.375rem !important;
    }
    
    /* Make multiselect dropdown items smaller */
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        font-size: 0.75rem !important;
        padding: 0.15rem 0.4rem !important;
        margin: 0.15rem !important;
        background-color: rgba(0, 153, 255, 0.2) !important;
        border: 1px solid rgba(0, 153, 255, 0.4) !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
        min-height: 36px !important;
        font-size: 0.8rem !important;
        padding: 0.25rem 0.5rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSlider {
        background: transparent;
        border-radius: 6px;
        padding: 0;
    }
    
    /* Sidebar selectbox compact styling */
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 0.75rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        font-size: 0.8rem !important;
        margin-bottom: 0.375rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        min-height: 36px !important;
        font-size: 0.8rem !important;
        padding: 0.25rem 0.5rem !important;
    }
    
    /* Sidebar info box - subtle professional style */
    [data-testid="stSidebar"] .stAlert {
        display: none;
    }
    
    /* Input fields - more compact */
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        color: #e5e7eb;
        font-size: 0.8rem !important;
        min-height: 36px !important;
    }
    
    /* Buttons - Professional style */
    .stButton > button {
        width: 100%;
        background: rgba(0, 153, 255, 0.15);
        color: #ffffff;
        border: 1px solid rgba(0, 153, 255, 0.3);
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: none;
        text-transform: none;
        letter-spacing: 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 153, 255, 0.2);
        background: rgba(0, 153, 255, 0.25);
        border-color: rgba(0, 153, 255, 0.4);
    }
    
    /* Expanders/Cards */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        margin-bottom: 1rem;
    }
    
    div[data-testid="stExpander"] summary {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Tables - Professional style */
    .dataframe {
        border: none !important;
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(10px);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    
    .dataframe thead tr th {
        background: rgba(0, 153, 255, 0.15) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.875rem !important;
        border: none !important;
        text-transform: none;
        letter-spacing: 0;
        font-size: 0.875rem;
    }
    
    .dataframe tbody tr {
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0, 153, 255, 0.08);
    }
    
    .dataframe tbody td {
        color: rgba(255, 255, 255, 0.9) !important;
        padding: 0.75rem 1rem !important;
    }
    
    /* Info/Alert boxes - subtle professional */
    .stAlert {
        background: rgba(0, 153, 255, 0.08);
        border-radius: 8px;
        border-left: 3px solid rgba(0, 153, 255, 0.5);
        padding: 0.875rem 1.25rem;
        box-shadow: none;
        backdrop-filter: blur(10px);
    }
    
    .stAlert p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.9rem;
    }
    
    /* Plotly charts container */
    .js-plotly-plot {
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    /* Ensure chart text is readable */
    .js-plotly-plot .plotly text {
        fill: #ffffff !important;
    }
    
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {
        fill: rgba(255, 255, 255, 0.9) !important;
    }
    
    .js-plotly-plot .plotly .colorbar text {
        fill: #ffffff !important;
    }
    
    /* Chart container spacing */
    div[data-testid="stPlotlyChart"] {
        margin: 1.5rem 0;
    }
    
    /* Tabs - Professional clean design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 0.375rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.65);
        font-weight: 500;
        padding: 0.625rem 1.25rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.85);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 153, 255, 0.2);
        color: #ffffff;
        border: 1px solid rgba(0, 153, 255, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: rgba(0, 153, 255, 0.8);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Divider */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.5), transparent);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0099ff 0%, #00d4ff 100%);
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.merged_df = None


def load_and_process_data():
    """Load and process all data using the DataProcessor."""
    # Define file paths
    base_path = Path(__file__).parent
    demographics_path = base_path / "data" / "demographics.csv"
    listings_path = base_path / "data" / "listings.csv"

    # Check if files exist
    if not demographics_path.exists() or not listings_path.exists():
        st.error("⚠️ Data files not found! Please ensure demographics.csv and listings.csv are in the data/ folder.")
        return None

    # Initialize processor
    processor = DataProcessor(
        str(demographics_path),
        str(listings_path)
    )

    # Process data
    with st.spinner("🔄 Processing data... This may take a moment."):
        merged_df = processor.process_all_data()

    if merged_df.empty:
        st.error("❌ Failed to process data. Please check the data files.")
        return None

    st.session_state.data_loaded = True
    st.session_state.merged_df = merged_df

    return merged_df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply user-selected filters to the dataframe.

    Args:
        df: Merged dataframe

    Returns:
        Filtered dataframe
    """
    filtered_df = df.copy()



    # ZIP Code filter
    with st.sidebar.expander("📮 ZIP Codes", expanded=False):
        if 'matched_zip_code' in df.columns:
            available_zips = sorted(df['matched_zip_code'].dropna().unique())
            selected_zips = st.multiselect(
                "Select ZIP Codes",
                options=available_zips,
                default=available_zips[:5] if len(available_zips) > 5 else available_zips,
                help="Filter properties by ZIP code",
                key="zip_filter"
            )
            if selected_zips:
                filtered_df = filtered_df[filtered_df['matched_zip_code'].isin(selected_zips)]

    # Price range filter
    with st.sidebar.expander("💰 Price Range", expanded=False):
        if 'listing_price' in df.columns:
            min_price = int(df['listing_price'].min())
            max_price = int(df['listing_price'].max())
            price_range = st.slider(
                "Listing Price ($)",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
                step=10000,
                help="Filter properties by listing price",
                key="price_filter"
            )
            filtered_df = filtered_df[
                (filtered_df['listing_price'] >= price_range[0]) &
                (filtered_df['listing_price'] <= price_range[1])
            ]

    # Bedrooms filter
    with st.sidebar.expander("🛏️ Bedrooms", expanded=False):
        if 'bedrooms' in df.columns:
            min_beds = int(df['bedrooms'].min())
            max_beds = int(df['bedrooms'].max())
            bedroom_range = st.slider(
                "Number of Bedrooms",
                min_value=min_beds,
                max_value=max_beds,
                value=(min_beds, max_beds),
                help="Filter by number of bedrooms",
                key="beds_filter"
            )
            filtered_df = filtered_df[
                (filtered_df['bedrooms'] >= bedroom_range[0]) &
                (filtered_df['bedrooms'] <= bedroom_range[1])
            ]

    # Square footage filter
    with st.sidebar.expander("📏 Square Footage", expanded=False):
        if 'sq_ft' in df.columns:
            min_sqft = int(df['sq_ft'].min())
            max_sqft = int(df['sq_ft'].max())
            sqft_range = st.slider(
                "Square Feet",
                min_value=min_sqft,
                max_value=max_sqft,
                value=(min_sqft, max_sqft),
                step=100,
                help="Filter properties by size",
                key="sqft_filter"
            )
            filtered_df = filtered_df[
                (filtered_df['sq_ft'] >= sqft_range[0]) &
                (filtered_df['sq_ft'] <= sqft_range[1])
            ]

    # Median income filter
    with st.sidebar.expander("💵 Median Income", expanded=False):
        if 'median_income' in df.columns:
            min_income = int(df['median_income'].min())
            max_income = int(df['median_income'].max())
            income_range = st.slider(
                "Income Range ($)",
                min_value=min_income,
                max_value=max_income,
                value=(min_income, max_income),
                step=5000,
                help="Filter by neighborhood median income",
                key="income_filter"
            )
            filtered_df = filtered_df[
                (filtered_df['median_income'] >= income_range[0]) &
                (filtered_df['median_income'] <= income_range[1])
            ]

    # School rating filter
    with st.sidebar.expander("🎓 School Rating", expanded=False):
        if 'school_rating' in df.columns:
            min_school = float(df['school_rating'].min())
            max_school = float(df['school_rating'].max())
            school_range = st.slider(
                "Rating (out of 10)",
                min_value=min_school,
                max_value=max_school,
                value=(min_school, max_school),
                step=0.5,
                help="Filter by school rating",
                key="school_filter"
            )
            filtered_df = filtered_df[
                (filtered_df['school_rating'] >= school_range[0]) &
                (filtered_df['school_rating'] <= school_range[1])
            ]

    # Crime index filter
    with st.sidebar.expander("🚨 Crime Level", expanded=False):
        if 'crime_index' in df.columns:
            crime_options = df['crime_index'].dropna().unique().tolist()
            selected_crime = st.multiselect(
                "Select Crime Levels",
                options=sorted(crime_options),
                default=crime_options,
                help="Filter by crime level",
                key="crime_filter"
            )
            if selected_crime:
                filtered_df = filtered_df[filtered_df['crime_index'].isin(selected_crime)]

    # Display filter results
    st.sidebar.markdown("---")
    st.sidebar.success(f"**{len(filtered_df):,}** / **{len(df):,}** properties")

    return filtered_df


def main():
    """Main application entry point."""
    
    # Professional sidebar header - compact
    st.sidebar.markdown("""
        <div style="margin-bottom: 1.25rem; padding-bottom: 0.875rem; border-bottom: 1px solid rgba(255,255,255,0.08);">
            <h2 style="margin: 0; color: #ffffff; font-size: 1.1rem; font-weight: 600; letter-spacing: -0.02em;">Filters</h2>
            <p style="margin: 0.375rem 0 0 0; color: #9ca3af; font-size: 0.8rem; line-height: 1.35;">Refine property search</p>
        </div>
    """, unsafe_allow_html=True)

    # Elegant Header with icon
    st.markdown("""
        <div style="text-align: center; padding: 1.25rem 0 0.75rem 0;">
            <h1 style="margin: 0; font-size: 2.25rem; font-weight: 700; letter-spacing: -0.02em; color: #ffffff;">
                🏠 Property Investment Insights
            </h1>
            <p style="font-size: 0.95rem; color: rgba(255,255,255,0.6); margin-top: 0.5rem; font-weight: 400;">
                Data-Driven Investment Decisions
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Load data
    if not st.session_state.data_loaded:
        merged_df = load_and_process_data()
        if merged_df is None:
            return
    else:
        merged_df = st.session_state.merged_df

    # Apply filters
    filtered_df = apply_filters(merged_df)

    # Initialize visualizer
    viz = Visualizer()

    # Calculate summary statistics
    stats = {
        'total_listings': len(filtered_df),
        'avg_price': filtered_df['listing_price'].mean(),
        'avg_price_per_sqft': filtered_df['price_per_sqft'].mean(),
        'avg_median_income': filtered_df['median_income'].mean(),
        'avg_sqft': filtered_df['sq_ft'].mean(),
        'avg_bedrooms': filtered_df['bedrooms'].mean(),
        'avg_school_rating': filtered_df['school_rating'].mean(),
        'unique_zip_codes': filtered_df['matched_zip_code'].nunique()
    }

    # Display KPIs
    st.markdown("## 📊 Key Performance Indicators")
    st.markdown("<br>", unsafe_allow_html=True)
    viz.display_kpi_metrics(stats)

    st.markdown("<br>", unsafe_allow_html=True)

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Market Analysis",
        "🎓 Demographics & Quality",
        "📍 Geographic Insights",
        "📋 Raw Data"
    ])

    # Tab 1: Market Analysis
    with tab1:
        st.markdown("### 💰 Market Analysis")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.plotly_chart(
                viz.create_price_distribution_chart(filtered_df),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                viz.create_property_size_distribution(filtered_df),
                use_container_width=True
            )

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.plotly_chart(
            viz.create_price_vs_income_scatter(filtered_df),
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

    # Tab 2: Demographics & Quality
    with tab2:
        st.markdown("### 🎓 Demographic & Quality Analysis")
        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(
            viz.create_school_rating_vs_price_chart(filtered_df),
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(
            viz.create_crime_index_analysis(filtered_df),
            use_container_width=True
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.plotly_chart(
            viz.create_price_to_income_ratio_chart(filtered_df),
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

    # Tab 3: Geographic Insights
    with tab3:
        st.markdown("### 📍 Geographic Distribution")
        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(
            viz.create_zip_code_heatmap(filtered_df),
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Simple map visualization (if coordinates available)
        st.info("💡 **Tip:** ZIP codes are visualized above. For precise geospatial mapping, integrate geocoding services to convert addresses to latitude/longitude.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Display top properties by value
        st.markdown("#### 🏆 Top Properties by Value")
        st.markdown("<br>", unsafe_allow_html=True)
        top_properties = filtered_df.nlargest(10, 'listing_price')[
            ['raw_address', 'matched_zip_code', 'listing_price', 
             'sq_ft', 'bedrooms', 'price_per_sqft', 
             'median_income', 'school_rating', 'crime_index']
        ].reset_index(drop=True)

        st.dataframe(
            top_properties,
            use_container_width=True,
            hide_index=True
        )

    # Tab 4: Raw Data
    with tab4:
        st.markdown("### 📋 Property Data Explorer")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        **Total Properties:** {len(filtered_df):,}  
        **Last Updated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Display full dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"property_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

        # Show data quality metrics
        with st.expander("📊 Data Quality Metrics"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Records",
                    f"{len(filtered_df):,}"
                )
            
            with col2:
                missing_pct = (filtered_df.isnull().sum().sum() / (len(filtered_df) * len(filtered_df.columns))) * 100
                st.metric(
                    "Missing Data %",
                    f"{missing_pct:.2f}%"
                )
            
            with col3:
                st.metric(
                    "Total Columns",
                    len(filtered_df.columns)
                )


if __name__ == "__main__":
    main()
