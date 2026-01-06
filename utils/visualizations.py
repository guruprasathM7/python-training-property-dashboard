"""
Visualization Module for Property Investment Insights Dashboard.

This module provides advanced interactive visualizations using Plotly
for geospatial mapping, KPI displays, and analytical charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Optional


class Visualizer:
    """Handles all visualization operations for the dashboard."""

    # Modern color scheme for dark theme
    COLOR_SCHEME = {
        'primary': '#00d4ff',
        'secondary': '#0099ff',
        'accent': '#00ffaa',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'info': '#8b5cf6',
        'gradient_start': '#00d4ff',
        'gradient_end': '#0099ff',
        'background': 'rgba(255, 255, 255, 0.05)',
        'text': '#ffffff',
    }
    
    # Plotly template for dark theme
    PLOTLY_TEMPLATE = {
        'layout': {
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font': {'color': '#ffffff', 'family': 'Inter, sans-serif'},
            'xaxis': {
                'gridcolor': 'rgba(255, 255, 255, 0.1)',
                'zerolinecolor': 'rgba(255, 255, 255, 0.1)',
            },
            'yaxis': {
                'gridcolor': 'rgba(255, 255, 255, 0.1)',
                'zerolinecolor': 'rgba(255, 255, 255, 0.1)',
            },
        }
    }

    @staticmethod
    def display_kpi_metrics(stats: dict) -> None:
        """
        Display key performance indicators in a metric grid.

        Args:
            stats: Dictionary of summary statistics
        """
        if not stats:
            st.warning("No data available for KPI display")
            return

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="📊 Total Listings",
                value=f"{stats.get('total_listings', 0):,}",
                help="Total number of property listings"
            )

        with col2:
            avg_price = stats.get('avg_price', 0)
            st.metric(
                label="💰 Avg Listing Price",
                value=f"${avg_price:,.0f}",
                help="Average listing price across all properties"
            )

        with col3:
            avg_price_sqft = stats.get('avg_price_per_sqft', 0)
            st.metric(
                label="📏 Avg Price/SqFt",
                value=f"${avg_price_sqft:,.2f}",
                help="Average price per square foot"
            )

        with col4:
            avg_income = stats.get('avg_median_income', 0)
            st.metric(
                label="💵 Avg Median Income",
                value=f"${avg_income:,.0f}",
                help="Average median income in the area"
            )

        # Second row of metrics
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            avg_sqft = stats.get('avg_sqft', 0)
            st.metric(
                label="🏠 Avg Square Feet",
                value=f"{avg_sqft:,.0f}",
                help="Average property size"
            )

        with col6:
            avg_beds = stats.get('avg_bedrooms', 0)
            st.metric(
                label="🛏️ Avg Bedrooms",
                value=f"{avg_beds:.1f}",
                help="Average number of bedrooms"
            )

        with col7:
            avg_school = stats.get('avg_school_rating', 0)
            st.metric(
                label="🎓 Avg School Rating",
                value=f"{avg_school:.1f}/10",
                help="Average school rating in the area"
            )

        with col8:
            unique_zips = stats.get('unique_zip_codes', 0)
            st.metric(
                label="📮 Unique ZIP Codes",
                value=f"{unique_zips}",
                help="Number of unique ZIP codes"
            )

    @staticmethod
    def create_price_distribution_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create histogram showing listing price distribution.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        fig = px.histogram(
            df,
            x='listing_price',
            nbins=30,
            title='<b>Distribution of Listing Prices</b>',
            labels={'listing_price': 'Listing Price ($)', 'count': 'Number of Properties'},
            color_discrete_sequence=[Visualizer.COLOR_SCHEME['primary']]
        )

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            showlegend=False,
            hovermode='x unified',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            margin=dict(l=80, r=60, t=100, b=80),
            height=650,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=11,
            yaxis_tickfont_size=11,
        )
        
        fig.update_xaxes(
            tickformat='$,.0f',
            tickangle=0,
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(color='rgba(0, 212, 255, 0.3)', width=1)
            ),
            hovertemplate='<b>Price Range</b>: $%{x:,.0f}<br><b>Count</b>: %{y}<extra></extra>'
        )

        return fig

    @staticmethod
    def create_price_vs_income_scatter(df: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot of listing price vs median income.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        # Filter out null values
        plot_df = df.dropna(subset=['listing_price', 'median_income', 'school_rating'])

        fig = px.scatter(
            plot_df,
            x='median_income',
            y='listing_price',
            size='sq_ft',
            color='school_rating',
            hover_data=['raw_address', 'bedrooms', 'price_per_sqft', 'crime_index'],
            title='<b>Listing Price vs Median Income</b>',
            labels={
                'median_income': 'Median Income ($)',
                'listing_price': 'Listing Price ($)',
                'school_rating': 'School Rating'
            },
            color_continuous_scale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']]
        )

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            hovermode='closest',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            margin=dict(l=80, r=120, t=100, b=80),
            height=650,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=11,
            yaxis_tickfont_size=11,
            coloraxis_colorbar=dict(
                title="School<br>Rating",
                title_font_size=11,
                tickfont_size=10,
                len=0.7,
                thickness=15,
                x=1.02,
            ),
        )
        
        fig.update_xaxes(
            tickformat='$,.0f',
            tickangle=0,
        )
        
        fig.update_yaxes(
            tickformat='$,.0f',
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(color='rgba(255, 255, 255, 0.2)', width=0.5),
                opacity=0.8,
                sizemin=3,
            ),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                          '<b>Income:</b> $%{x:,.0f}<br>' +
                          '<b>Price:</b> $%{y:,.0f}<br>' +
                          '<b>Bedrooms:</b> %{customdata[1]}<br>' +
                          '<b>Price/SqFt:</b> $%{customdata[2]:.2f}<br>' +
                          '<b>Crime:</b> %{customdata[3]}<extra></extra>'
        )

        return fig

    @staticmethod
    def create_school_rating_vs_price_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot showing relationship between school ratings and prices.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        plot_df = df.dropna(subset=['school_rating', 'listing_price'])

        fig = px.scatter(
            plot_df,
            x='school_rating',
            y='listing_price',
            color='crime_index',
            size='sq_ft',
            hover_data=['raw_address', 'bedrooms', 'median_income'],
            title='<b>School Rating vs Listing Price</b>',
            labels={
                'school_rating': 'School Rating (out of 10)',
                'listing_price': 'Listing Price ($)',
                'crime_index': 'Crime Level'
            },
            color_discrete_map={
                'Low': Visualizer.COLOR_SCHEME['success'],
                'Medium': Visualizer.COLOR_SCHEME['secondary'],
                'High': Visualizer.COLOR_SCHEME['warning']
            }
        )

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            hovermode='closest',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            margin=dict(l=80, r=60, t=100, b=80),
            height=650,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=11,
            yaxis_tickfont_size=11,
            legend=dict(
                title_font_size=12,
                font_size=11,
                bgcolor='rgba(0, 0, 0, 0.3)',
                bordercolor='rgba(255, 255, 255, 0.2)',
                borderwidth=1,
            ),
        )
        
        fig.update_xaxes(range=[0, 10.5])
        fig.update_yaxes(tickformat='$,.0f')
        
        fig.update_traces(
            marker=dict(
                line=dict(color='rgba(255, 255, 255, 0.3)', width=0.5),
                opacity=0.7,
                sizemin=3,
            )
        )

        return fig

    @staticmethod
    def create_property_size_distribution(df: pd.DataFrame) -> go.Figure:
        """
        Create box plot showing property size distribution by bedrooms.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        plot_df = df.dropna(subset=['bedrooms', 'sq_ft'])
        plot_df['bedrooms'] = plot_df['bedrooms'].astype(int)

        fig = px.box(
            plot_df,
            x='bedrooms',
            y='sq_ft',
            color='bedrooms',
            title='<b>Property Size Distribution by Bedrooms</b>',
            labels={
                'bedrooms': 'Number of Bedrooms',
                'sq_ft': 'Square Feet'
            }
        )

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            showlegend=False,
            hovermode='x unified',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            margin=dict(l=80, r=60, t=100, b=80),
            height=650,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=11,
            yaxis_tickfont_size=11,
        )
        
        fig.update_yaxes(tickformat=',')
        
        fig.update_traces(
            marker=dict(opacity=0.7, line=dict(color='rgba(255, 255, 255, 0.3)', width=1)),
            boxmean=True,
        )

        return fig

    @staticmethod
    def create_crime_index_analysis(df: pd.DataFrame) -> go.Figure:
        """
        Create bar chart analyzing average prices by crime index.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        plot_df = df.dropna(subset=['crime_index', 'listing_price'])

        avg_by_crime = plot_df.groupby('crime_index').agg({
            'listing_price': 'mean',
            'price_per_sqft': 'mean',
            'school_rating': 'mean'
        }).reset_index()

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Avg Price by Crime Level', 'Avg Price/SqFt by Crime Level')
        )

        # Crime order
        crime_order = ['Low', 'Medium', 'High']
        avg_by_crime['crime_index'] = pd.Categorical(
            avg_by_crime['crime_index'],
            categories=crime_order,
            ordered=True
        )
        avg_by_crime = avg_by_crime.sort_values('crime_index')

        colors = [
            Visualizer.COLOR_SCHEME['success'],
            Visualizer.COLOR_SCHEME['secondary'],
            Visualizer.COLOR_SCHEME['warning']
        ]

        fig.add_trace(
            go.Bar(
                x=avg_by_crime['crime_index'],
                y=avg_by_crime['listing_price'],
                marker_color=colors[:len(avg_by_crime)],
                name='Avg Price'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=avg_by_crime['crime_index'],
                y=avg_by_crime['price_per_sqft'],
                marker_color=colors[:len(avg_by_crime)],
                name='Avg Price/SqFt'
            ),
            row=1, col=2
        )

        fig.update_xaxes(title_text="Crime Level", row=1, col=1)
        fig.update_xaxes(title_text="Crime Level", row=1, col=2)
        fig.update_yaxes(title_text="Avg Listing Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Avg Price per SqFt ($)", row=1, col=2)

        fig.update_layout(
            title_text="Property Value Analysis by Crime Index",
            showlegend=False,
            plot_bgcolor='white',
            title_font_size=16,
            height=600
        )

        return fig

    @staticmethod
    def create_zip_code_heatmap(df: pd.DataFrame) -> go.Figure:
        """
        Create heatmap showing property metrics by ZIP code.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        plot_df = df.dropna(subset=['matched_zip_code'])

        # Aggregate by ZIP code
        zip_stats = plot_df.groupby('matched_zip_code').agg({
            'listing_price': 'mean',
            'median_income': 'mean',
            'school_rating': 'mean',
            'price_per_sqft': 'mean',
            'raw_address': 'count'
        }).reset_index()

        zip_stats.columns = [
            'ZIP Code', 'Avg Price', 'Median Income',
            'Avg School Rating', 'Avg Price/SqFt', 'Property Count'
        ]

        # Sort by property count
        zip_stats = zip_stats.sort_values('Property Count', ascending=False).head(15)

        fig = px.bar(
            zip_stats,
            x='ZIP Code',
            y='Property Count',
            color='Avg Price',
            hover_data=['Median Income', 'Avg School Rating', 'Avg Price/SqFt'],
            title='<b>Top 15 ZIP Codes by Property Count</b>',
            labels={'Property Count': 'Number of Properties'},
            color_continuous_scale=[[0, '#00d4ff'], [0.5, '#0099ff'], [1, '#8b5cf6']]
        )

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            xaxis_tickangle=-45,
            hovermode='x unified',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            margin=dict(l=80, r=120, t=100, b=120),
            height=650,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=10,
            yaxis_tickfont_size=11,
            coloraxis_colorbar=dict(
                title="Avg<br>Price",
                title_font_size=11,
                tickfont_size=10,
                tickformat='$,.0f',
                len=0.7,
                thickness=15,
                x=1.02,
            ),
        )
        
        fig.update_yaxes(tickformat=',')
        
        fig.update_traces(
            marker=dict(
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            hovertemplate='<b>ZIP: %{x}</b><br>' +
                          '<b>Properties:</b> %{y}<br>' +
                          '<b>Avg Price:</b> $%{customdata[0]:,.0f}<br>' +
                          '<b>Median Income:</b> $%{customdata[1]:,.0f}<br>' +
                          '<b>School Rating:</b> %{customdata[2]:.1f}<br>' +
                          '<b>Price/SqFt:</b> $%{customdata[3]:.2f}<extra></extra>'
        )

        return fig

    @staticmethod
    def create_price_to_income_ratio_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create chart showing price-to-income ratios by ZIP code.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        plot_df = df.dropna(subset=['matched_zip_code', 'price_to_income_ratio'])

        # Calculate average ratio by ZIP
        zip_ratio = plot_df.groupby('matched_zip_code').agg({
            'price_to_income_ratio': 'mean',
            'raw_address': 'count'
        }).reset_index()

        zip_ratio.columns = ['ZIP Code', 'Avg Price-to-Income Ratio', 'Property Count']

        # Filter ZIPs with at least 3 properties
        zip_ratio = zip_ratio[zip_ratio['Property Count'] >= 3]
        zip_ratio = zip_ratio.sort_values('Avg Price-to-Income Ratio', ascending=False).head(15)

        fig = px.bar(
            zip_ratio,
            x='ZIP Code',
            y='Avg Price-to-Income Ratio',
            color='Avg Price-to-Income Ratio',
            hover_data=['Property Count'],
            title='<b>Price-to-Income Ratio by ZIP Code (Top 15)</b>',
            labels={'Avg Price-to-Income Ratio': 'Avg Price/Income Ratio'},
            color_continuous_scale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']]
        )

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            xaxis_tickangle=-45,
            hovermode='x unified',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            margin=dict(l=80, r=120, t=100, b=120),
            height=650,
            xaxis_title_font_size=13,
            yaxis_title_font_size=13,
            xaxis_tickfont_size=10,
            yaxis_tickfont_size=11,
            coloraxis_colorbar=dict(
                title="Ratio",
                title_font_size=11,
                tickfont_size=10,
                len=0.7,
                thickness=15,
                x=1.02,
            ),
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            hovertemplate='<b>ZIP: %{x}</b><br>' +
                          '<b>Ratio:</b> %{y:.2f}x<br>' +
                          '<b>Properties:</b> %{customdata[0]}<extra></extra>'
        )

        return fig

    @staticmethod
    def create_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
        """
        Create correlation heatmap for numerical variables.

        Args:
            df: Processed dataframe

        Returns:
            Plotly figure object
        """
        # Select numerical columns
        numerical_cols = [
            'listing_price', 'sq_ft', 'bedrooms',
            'median_income', 'school_rating', 'price_per_sqft'
        ]

        # Filter available columns
        available_cols = [col for col in numerical_cols if col in df.columns]
        corr_df = df[available_cols].corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns,
            y=corr_df.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_df.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 11, "color": "white"},
            colorbar=dict(
                title="Correlation",
                title_font_size=11,
                tickfont_size=10,
                len=0.7,
                thickness=15,
            )
        ))

        fig.update_layout(
            **Visualizer.PLOTLY_TEMPLATE['layout'],
            title='<b>Correlation Matrix: Property & Demographic Features</b>',
            title_font_size=16,
            title_font_color='#ffffff',
            title_x=0.5,
            title_xanchor='center',
            xaxis_tickangle=-45,
            height=700,
            margin=dict(l=100, r=60, t=100, b=120),
            xaxis_tickfont_size=11,
            yaxis_tickfont_size=11,
        )

        return fig
