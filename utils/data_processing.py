"""
Data Processing Module for Property Investment Insights Dashboard.

This module handles data loading, cleaning, and merging with advanced
fuzzy matching capabilities to resolve inconsistent address formatting.
"""

import re
import pandas as pd
import streamlit as st
from rapidfuzz import fuzz, process
from typing import Tuple, Optional


class DataProcessor:
    """Handles all data processing operations for the dashboard."""

    def __init__(self, demographics_path: str, listings_path: str):
        """
        Initialize the DataProcessor with file paths.

        Args:
            demographics_path: Path to demographics CSV file
            listings_path: Path to listings CSV file
        """
        self.demographics_path = demographics_path
        self.listings_path = listings_path
        self.demographics_df = None
        self.listings_df = None
        self.merged_df = None

    @st.cache_data(ttl=3600)
    def load_data(_self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load data from CSV files with caching for performance.

        Returns:
            Tuple of (demographics_df, listings_df)
        """
        try:
            demographics_df = pd.read_csv(_self.demographics_path)
            listings_df = pd.read_csv(_self.listings_path)
            return demographics_df, listings_df
        except FileNotFoundError as e:
            st.error(f"Error loading data files: {e}")
            return pd.DataFrame(), pd.DataFrame()

    @staticmethod
    def normalize_postal_code(postal_code: str) -> str:
        """
        Normalize postal codes handling various formats including 'XX' patterns.

        Args:
            postal_code: Raw postal code string

        Returns:
            Normalized postal code or None if invalid
        """
        if pd.isna(postal_code):
            return None

        postal_str = str(postal_code).strip().upper()

        # Handle patterns like '325XX', '150XX' - extract first 3 digits
        if 'XX' in postal_str or 'X' in postal_str:
            digits = re.findall(r'\d+', postal_str)
            if digits:
                return digits[0][:5].zfill(5)

        # Extract digits only
        digits_only = re.sub(r'\D', '', postal_str)

        if len(digits_only) >= 5:
            return digits_only[:5]
        elif len(digits_only) > 0:
            return digits_only.zfill(5)

        return None

    @staticmethod
    def normalize_address(address: str) -> str:
        """
        Normalize address strings for consistent comparison.

        Handles:
        - Case inconsistencies
        - Abbreviations (St., Blvd., Ave., etc.)
        - Extra whitespace
        - Special characters

        Args:
            address: Raw address string

        Returns:
            Normalized address string
        """
        if pd.isna(address):
            return ""

        # Convert to lowercase
        addr = str(address).lower().strip()

        # Remove extra whitespace
        addr = re.sub(r'\s+', ' ', addr)

        # Standardize common abbreviations
        replacements = {
            r'\bst\.?\b': 'street',
            r'\bave\.?\b': 'avenue',
            r'\bavenue\b': 'avenue',
            r'\bstravenue\b': 'street',  # Handle 'stravenue' edge case
            r'\bblvd\.?\b': 'boulevard',
            r'\brd\.?\b': 'road',
            r'\bdr\.?\b': 'drive',
            r'\bln\.?\b': 'lane',
            r'\bct\.?\b': 'court',
            r'\bpl\.?\b': 'place',
            r'\bpkwy\.?\b': 'parkway',
            r'\bcir\.?\b': 'circle',
            r'\bsq\.?\b': 'square',
            r'\bsquares\b': 'square',
            r'\bjunction\.?s?\b': 'junction',
            r'\btrack\b': 'tract',  # Common typo
            r'\bwalk\b': 'walk',
            r'\bbypass\b': 'bypass',
            r'\bradial\b': 'radial',
            r'\bfort\b': 'fort',
            r'\blight\b': 'light',
            r'\bstream\b': 'stream',
            r'\bvillage\b': 'village',
            r'\bknoll\b': 'knoll',
            r'\bkey\b': 'key',
            r'\bfork\.?s?\b': 'fork',
        }

        for pattern, replacement in replacements.items():
            addr = re.sub(pattern, replacement, addr)

        # Remove punctuation except spaces
        addr = re.sub(r'[^\w\s]', '', addr)

        # Remove duplicate words
        words = addr.split()
        # Keep first occurrence of each word in sequence
        seen = set()
        result = []
        for word in words:
            if word not in seen or word.isdigit():
                result.append(word)
                seen.add(word)

        return ' '.join(result)

    def clean_listings_data(self, listings_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize listings data.

        Args:
            listings_df: Raw listings dataframe

        Returns:
            Cleaned listings dataframe
        """
        df = listings_df.copy()

        # Normalize postal codes
        df['postal_code_normalized'] = df['postal_code'].apply(
            self.normalize_postal_code
        )

        # Normalize addresses
        df['address_normalized'] = df['raw_address'].apply(
            self.normalize_address
        )

        # Handle null values
        df['sq_ft'] = pd.to_numeric(df['sq_ft'], errors='coerce')
        df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')
        df['listing_price'] = pd.to_numeric(df['listing_price'], errors='coerce')

        # Remove rows with invalid data
        df = df.dropna(subset=['listing_price', 'sq_ft'])

        # Calculate price per sq ft
        df['price_per_sqft'] = (
            df['listing_price'] / df['sq_ft']
        ).round(2)

        return df

    def clean_demographics_data(self, demographics_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize demographics data.

        Args:
            demographics_df: Raw demographics dataframe

        Returns:
            Cleaned demographics dataframe
        """
        df = demographics_df.copy()

        # Normalize zip codes to string
        df['zip_code'] = df['zip_code'].astype(str).str.zfill(5)

        # Handle numeric columns
        df['median_income'] = pd.to_numeric(df['median_income'], errors='coerce')
        df['school_rating'] = pd.to_numeric(df['school_rating'], errors='coerce')

        # Standardize crime_index values
        df['crime_index'] = df['crime_index'].str.strip().str.title()

        return df

    def fuzzy_match_postal_codes(
        self,
        listings_df: pd.DataFrame,
        demographics_df: pd.DataFrame,
        threshold: int = 80
    ) -> pd.DataFrame:
        """
        Match postal codes using fuzzy matching with Levenshtein distance.

        Handles cases where postal codes are partially masked (e.g., '325XX').

        Args:
            listings_df: Cleaned listings dataframe
            demographics_df: Cleaned demographics dataframe
            threshold: Minimum similarity score (0-100)

        Returns:
            Listings dataframe with matched zip codes
        """
        df = listings_df.copy()

        # Get list of valid zip codes from demographics
        valid_zips = demographics_df['zip_code'].unique().tolist()

        def find_best_match(postal_code):
            """Find best matching zip code using fuzzy matching."""
            if pd.isna(postal_code):
                return None

            postal_str = str(postal_code)

            # First try exact match
            if postal_str in valid_zips:
                return postal_str

            # Try fuzzy matching
            result = process.extractOne(
                postal_str,
                valid_zips,
                scorer=fuzz.ratio,
                score_cutoff=threshold
            )

            if result:
                return result[0]

            return None

        df['matched_zip_code'] = df['postal_code_normalized'].apply(
            find_best_match
        )

        return df

    def merge_data(
        self,
        listings_df: pd.DataFrame,
        demographics_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge listings and demographics data.

        Args:
            listings_df: Cleaned listings dataframe with matched zip codes
            demographics_df: Cleaned demographics dataframe

        Returns:
            Merged dataframe
        """
        # Merge on matched zip codes
        merged = pd.merge(
            listings_df,
            demographics_df,
            left_on='matched_zip_code',
            right_on='zip_code',
            how='left'
        )

        # Calculate additional metrics
        if 'median_income' in merged.columns and 'listing_price' in merged.columns:
            merged['price_to_income_ratio'] = (
                merged['listing_price'] / merged['median_income']
            ).round(2)

        return merged

    def process_all_data(self) -> pd.DataFrame:
        """
        Execute complete data processing pipeline.

        Returns:
            Fully processed and merged dataframe
        """
        # Load data
        demographics_df, listings_df = self.load_data()

        if demographics_df.empty or listings_df.empty:
            st.error("Failed to load data files. Please check the data directory.")
            return pd.DataFrame()

        # Clean data
        listings_clean = self.clean_listings_data(listings_df)
        demographics_clean = self.clean_demographics_data(demographics_df)

        # Fuzzy match postal codes
        listings_matched = self.fuzzy_match_postal_codes(
            listings_clean,
            demographics_clean
        )

        # Merge data
        merged_df = self.merge_data(listings_matched, demographics_clean)

        self.merged_df = merged_df
        return merged_df

    def get_summary_statistics(self, df: pd.DataFrame) -> dict:
        """
        Calculate summary statistics for the dashboard.

        Args:
            df: Processed dataframe

        Returns:
            Dictionary of summary statistics
        """
        if df.empty:
            return {}

        stats = {
            'total_listings': len(df),
            'avg_price': df['listing_price'].mean(),
            'avg_price_per_sqft': df['price_per_sqft'].mean(),
            'avg_sqft': df['sq_ft'].mean(),
            'avg_bedrooms': df['bedrooms'].mean(),
            'avg_median_income': df['median_income'].mean() if 'median_income' in df.columns else 0,
            'avg_school_rating': df['school_rating'].mean() if 'school_rating' in df.columns else 0,
            'unique_zip_codes': df['matched_zip_code'].nunique(),
        }

        return stats
