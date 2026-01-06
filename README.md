# 🏠 Property Investment Insights Dashboard

> **Kantar Python Capstone Project - January 2026**  
> Professional Streamlit dashboard for property investment analysis with advanced fuzzy matching and interactive visualizations.

**🔗 GitHub Repository:** [https://github.com/guruprasathM7/python-training-property-dashboard](https://github.com/guruprasathM7/python-training-property-dashboard)

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🚀 Quick Start](#-quick-start)
- [📦 Deliverables](#-deliverables)
- [⚙️ Technical Stack](#️-technical-stack)
- [📸 Dashboard Screenshots](#-dashboard-screenshots)
- [✨ Key Features](#-key-features)
- [📊 Data Processing](#-data-processing)
---

## 🎯 Overview

Interactive dashboard integrating real estate listings with demographic data, resolving inconsistent address formats through fuzzy matching algorithms to provide actionable investment insights.

**Key Challenge:** Merge messy street-level listings with structured demographic databases  
**Solution:** Advanced fuzzy matching with 90%+ success rate using RapidFuzz

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/guruprasathM7/python-training-property-dashboard.git
cd python-training-property-dashboard

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 📦 Deliverables

### ✅ 1. app.py (Main Streamlit Application)
- **890+ lines** of clean, professional code
- Modular architecture with custom CSS styling
- Real-time filtering and interactive visualizations
- PEP 8 compliant with comprehensive docstrings

### ✅ 2. requirements.txt (Dependencies)
```
streamlit==1.31.0
pandas==2.1.4
plotly==5.18.0
rapidfuzz==3.6.1
```
One-command installation: `pip install -r requirements.txt`

### ✅ 3. Screenshots (assets/ folder)
7 high-resolution captures showcasing all dashboard features

### ✅ 4. Standard Folder Structure
```
python-training-property-dashboard/
├── app.py                    # Main application (890+ lines)
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── data/                     # CSV data files
│   ├── demographics.csv      # Demographic data by ZIP
│   └── listings.csv          # Property listings
├── utils/                    # Utility modules
│   ├── data_processing.py    # Fuzzy matching & merging
│   └── visualizations.py     # Plotly charts
└── assets/                   # Screenshots (7 images)
```

### ✅ 5. Clean Linted Code
- PEP 8 compliant formatting
- Type hints throughout
- Comprehensive docstrings
- Modular design with separation of concerns
- Zero linting errors

---

## ⚙️ Technical Stack

- **Python 3.11+** - Core language
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **RapidFuzz** - Fuzzy string matching (Levenshtein distance)
- **Plotly** - Interactive visualizations

---

## 📸 Dashboard Screenshots

![Dashboard Overview](assets/1.png)
*Complete property investment dashboard with KPIs, filters, and interactive visualizations*

![Market Analysis](assets/2.png)
*Comprehensive market analytics with price distributions and property size insights*

![Demographics Analysis](assets/3.png)
*Correlation analysis between neighborhood quality and property values*

![Geographic Distribution](assets/4.png)
*Visual representation of property distribution across ZIP codes*

![Data Explorer](assets/5.png)
*Complete dataset with filtering and export capabilities*

![Advanced Filters](assets/6.png)
*Intuitive sidebar with comprehensive filtering options*

![Interactive Charts](assets/7.png)
*Dynamic charts with hover details and real-time updates*

---

## ✨ Key Features

- **Fuzzy Matching Engine:** Resolves inconsistent addresses with 90%+ accuracy
- **8 KPI Metrics:** Real-time property statistics
- **9+ Interactive Charts:** Plotly visualizations with hover details
- **Advanced Filters:** ZIP code, price range, bedrooms, demographics, crime index
- **4 Analysis Tabs:** Market, Demographics, Geographic, Raw Data
- **Data Export:** CSV download functionality
- **Professional UI:** Custom CSS, dark theme, responsive design

---

## 📊 Data Processing

1. **Address Normalization:** Standardize inconsistent address formats
2. **Fuzzy Matching:** RapidFuzz with 80% similarity threshold
3. **Data Merging:** Left join on ZIP codes with derived metrics
4. **Performance:** Cached data loading with `@st.cache_data`

---

