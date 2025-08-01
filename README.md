# HealthKart Influencer Campaign Dashboard 📊

A comprehensive analytics dashboard for tracking and optimizing influencer marketing campaigns across multiple platforms and brands.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

This dashboard provides real-time insights into influencer campaign performance, helping HealthKart optimize their marketing spend across MuscleBlaze, HKVitals, and Gritzo brands. Track ROAS, identify top performers, and make data-driven decisions to maximize ROI.

## ✨ Features

### 📈 Core Analytics
- **Campaign Performance Tracking**: Monitor reach, engagement, and conversion metrics
- **ROAS Calculation**: Track Return on Ad Spend and incremental ROAS
- **Multi-Platform Analysis**: Compare performance across Instagram, YouTube, and Twitter
- **Brand Performance**: Analyze campaign effectiveness by brand (MuscleBlaze, HKVitals, Gritzo)

### 🔍 Advanced Insights
- **Influencer Ranking**: Identify top and underperforming influencers
- **Engagement Analysis**: Track likes, comments, and engagement rates
- **Revenue Attribution**: Track orders and revenue back to specific posts
- **Payout Optimization**: Monitor different payout models (per post vs per order)

### 📊 Interactive Features
- **Dynamic Filtering**: Filter by brand, platform, category, and date range
- **Real-time Updates**: Dashboard updates automatically with filter changes
- **Export Functionality**: Download data as CSV for further analysis
- **Visual Analytics**: Interactive charts and graphs using Plotly

## 🏗️ Data Model

### Core Tables

#### 1. Influencers
```python
{
    'id': int,              # Unique influencer identifier
    'name': str,            # Influencer handle/name
    'category': str,        # Content category (Fitness, Nutrition, etc.)
    'gender': str,          # Gender classification
    'follower_count': int,  # Number of followers
    'platform': str         # Primary platform (Instagram, YouTube, Twitter)
}
```

#### 2. Posts
```python
{
    'influencer_id': int,   # Foreign key to influencers
    'platform': str,        # Platform where post was published
    'date': datetime,       # Post publication date
    'url': str,            # Post URL
    'caption': str,        # Post caption/description
    'reach': int,          # Number of unique users reached
    'likes': int,          # Number of likes
    'comments': int,       # Number of comments
    'brand': str          # Associated brand
}
```

#### 3. Tracking Data
```python
{
    'source': str,         # Traffic source (Instagram, YouTube, Twitter)
    'campaign': str,       # Campaign identifier
    'influencer_id': int,  # Foreign key to influencers
    'user_id': int,        # Customer identifier
    'product': str,        # Product purchased
    'brand': str,          # Brand of the product
    'date': datetime,      # Purchase date
    'orders': int,         # Number of orders (usually 1)
    'revenue': float       # Revenue generated (INR)
}
```

#### 4. Payouts
```python
{
    'influencer_id': int,  # Foreign key to influencers
    'basis': str,          # Payment basis ('post' or 'order')
    'rate': float,         # Rate per post or per order (INR)
    'orders': int,         # Number of orders (if basis is 'order')
    'total_payout': float  # Total amount paid (INR)
}
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/healthkart-dashboard.git
cd healthkart-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run dashboard.py
```

4. **Access the dashboard**
Open your browser and navigate to `http://localhost:8501`

### Dependencies
```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.15.0
datetime
```

## 📊 Key Metrics Explained

### ROAS (Return on Ad Spend)
```
ROAS = Total Revenue / Total Ad Spend
```
- **Good ROAS**: > 3.0x (₹3 revenue for every ₹1 spent)
- **Average ROAS**: 2.0x - 3.0x
- **Poor ROAS**: < 2.0x

### Incremental ROAS
```
Incremental ROAS = (Total Revenue × 0.8) / Total Ad Spend
```
Assumes 20% of sales would have happened without the campaign (baseline conversion).

### Engagement Rate
```
Engagement Rate = (Likes + Comments) / Reach × 100
```
- **High Engagement**: > 3%
- **Average Engagement**: 1% - 3%
- **Low Engagement**: < 1%

## 🎨 Dashboard Sections

### 1. Key Performance Metrics
- Total Revenue generated
- Overall ROAS across all campaigns
- Total Reach achieved
- Average Engagement Rate

### 2. Performance Analysis
- **Top Influencers by ROAS**: Bar chart showing best performers
- **Revenue by Platform**: Pie chart of platform distribution
- **Daily Revenue Trend**: Time series of revenue performance
- **Brand Performance**: Comparative analysis across brands

### 3. Influencer Insights
- **Top Performers Table**: Detailed metrics for best influencers
- **Underperforming Influencers**: List of campaigns needing attention
- **Category Analysis**: Performance by influencer category

### 4. Detailed Analytics
- **Posts Analytics**: Detailed post-level performance data
- **Revenue Tracking**: Order-level attribution data
- **Payout Summary**: Payment details for all influencers
- **Export Functions**: Download data for external analysis

## 🔧 Configuration & Customization

### Adding New Data Sources
To integrate real data sources, modify the `generate_sample_data()` function:

```python
@st.cache_data
def load_real_data():
    # Replace with your data loading logic
    influencers_df = pd.read_csv('path/to/influencers.csv')
    posts_df = pd.read_csv('path/to/posts.csv')
    tracking_df = pd.read_csv('path/to/tracking.csv')
    payouts_df = pd.read_csv('path/to/payouts.csv')
    
    return influencers_df, posts_df, tracking_df, payouts_df
```

### Custom Metrics
Add new metrics by modifying the `calculate_roas_metrics()` function:

```python
def calculate_custom_metrics(data):
    # Add your custom calculations here
    data['cpm'] = data['total_payout'] / (data['reach'] / 1000)
    data['cpc'] = data['total_payout'] / data['clicks']
    return data
```

### Styling Customization
Modify the CSS in the `st.markdown()` section to change colors, fonts, and layout.

## 📈 Sample Insights

The dashboard generates realistic sample data showing:

- **15 influencers** across 5 categories (Fitness, Nutrition, Wellness, Bodybuilding, Yoga)
- **200+ posts** across Instagram, YouTube, and Twitter
- **Revenue tracking** for 3
