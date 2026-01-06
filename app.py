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
    initial_sidebar_state="auto"
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
    
    /* Hide the collapse button */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    button[kind="header"] {
        display: none !important;
    }
    
    /* Force sidebar toggle button to be visible */
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        background-color: #00d4ff !important;
        color: white !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 1rem 0.5rem !important;
        font-size: 1.5rem !important;
        z-index: 9999 !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background-color: #0099ff !important;
        transform: scale(1.1);
    }
    
    /* Main container with gradient */
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Metrics - Clean card design */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem;
        font-weight: 600;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Headers - Modern typography */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-left: 1rem;
        border-left: 4px solid #00d4ff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    h3 {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        margin-top: 1.5rem !important;
    }
    
    /* Sidebar - Dark elegant */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        min-width: 280px !important;
        max-width: 320px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
        padding: 1rem 0.75rem;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.3rem !important;
        margin-bottom: 0.5rem !important;
        padding: 0.5rem;
        background: rgba(0, 212, 255, 0.1);
        border-radius: 8px;
        text-align: center;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
        font-size: 0.8rem;
        line-height: 1.4;
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-size: 0.95rem !important;
        margin: 0.5rem 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem !important;
    }
    
    /* Compact expanders in sidebar */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        padding: 0;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        font-size: 0.85rem !important;
        padding: 0.5rem 0.75rem !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] > div {
        padding: 0.5rem 0.75rem !important;
    }
    
    /* Compact sliders */
    [data-testid="stSidebar"] .stSlider {
        padding: 0.25rem 0;
    }
    
    [data-testid="stSidebar"] .stSlider label {
        font-size: 0.7rem !important;
    }
    
    /* Compact multiselect */
    [data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stMultiSelect label {
        font-size: 0.7rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSlider {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
        padding: 0.25rem;
    }
    
    /* Sidebar info box */
    [data-testid="stSidebar"] .stAlert {
        padding: 0.5rem 0.75rem;
        font-size: 0.8rem;
        margin: 0.5rem 0;
    }
    
    /* Input fields */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #ffffff;
    }
    
    /* Buttons - Gradient accent */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
        background: linear-gradient(135deg, #0099ff 0%, #00d4ff 100%);
    }
    
    /* Expanders/Cards */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
    }
    
    div[data-testid="stExpander"] summary {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Tables - Clean and modern */
    .dataframe {
        border: none !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85rem;
    }
    
    .dataframe tbody tr {
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0, 212, 255, 0.1);
    }
    
    .dataframe tbody td {
        color: rgba(255, 255, 255, 0.9) !important;
        padding: 0.75rem 1rem !important;
    }
    
    /* Info/Alert boxes */
    .stAlert {
        background: rgba(0, 212, 255, 0.1);
        border-radius: 12px;
        border-left: 4px solid #00d4ff;
        padding: 1rem 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stAlert p {
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Plotly charts container */
    .js-plotly-plot {
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.05);
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%);
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
    
    # Compact sidebar header
    st.sidebar.title("Filters")
    st.sidebar.markdown("---")

    # Elegant Header with icon
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.5px;">
                🏠 Property Investment Insights
            </h1>
            <p style="font-size: 1rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem; font-weight: 400;">
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
    viz.display_kpi_metrics(stats)

    st.markdown("---")

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Market Analysis",
        "🎓 Demographics & Quality",
        "📍 Geographic Insights",
        "📋 Raw Data"
    ])

    # Tab 1: Market Analysis
    with tab1:
        st.markdown("## 💰 Market Analysis")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")

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
        st.markdown("## 🎓 Demographic & Quality Analysis")
        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(
            viz.create_school_rating_vs_price_chart(filtered_df),
            use_container_width=True
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

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
        st.markdown("## 📍 Geographic Distribution")
        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(
            viz.create_zip_code_heatmap(filtered_df),
            use_container_width=True
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Simple map visualization (if coordinates available)
        st.info("💡 **Pro Tip:** ZIP codes are visualized above. For precise geospatial mapping, "
                "integrate geocoding services to convert addresses to latitude/longitude.")

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Display top properties by value
        st.markdown("### 🏆 Top Properties by Value")
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
        st.markdown("## 📋 Property Data Explorer")
        
        st.markdown(f"""
        **Total Properties:** {len(filtered_df):,}  
        **Date Processed:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)

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
