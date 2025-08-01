import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="HealthKart Influencer Campaign Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric > div > div > div > div {
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Generation Functions
@st.cache_data
def generate_sample_data():
    """Generate realistic sample data for the dashboard"""
    
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate influencers data
    influencer_names = [
        "FitnessFrida", "HealthGuru_Sam", "YogaQueen_Maya", "ProteinPro_Raj",
        "WellnessWarrior", "FitLife_Arya", "MuscleMania_Dev", "HealthyHabits_Ria",
        "FitnessFirst_Karan", "NutriNinja_Priya", "GymBeast_Rohit", "WellnessWiz_Sanya",
        "FitnessFanatic_Amit", "HealthHub_Neha", "ProteinPower_Vikram"
    ]
    
    categories = ["Fitness", "Nutrition", "Wellness", "Bodybuilding", "Yoga"]
    genders = ["Male", "Female", "Other"]
    platforms = ["Instagram", "YouTube", "Twitter"]
    
    influencers_data = []
    for i, name in enumerate(influencer_names):
        influencers_data.append({
            'id': i + 1,
            'name': name,
            'category': random.choice(categories),
            'gender': random.choice(genders),
            'follower_count': random.randint(10000, 5000000),
            'platform': random.choice(platforms)
        })
    
    influencers_df = pd.DataFrame(influencers_data)
    
    # Generate posts data
    posts_data = []
    brands = ["MuscleBlaze", "HKVitals", "Gritzo"]
    
    for _ in range(200):  # Generate 200 posts
        influencer_id = random.randint(1, len(influencer_names))
        platform = random.choice(platforms)
        date = datetime.now() - timedelta(days=random.randint(1, 90))
        
        # Simulate realistic engagement based on follower count
        influencer_followers = influencers_df[influencers_df['id'] == influencer_id]['follower_count'].iloc[0]
        reach = int(influencer_followers * random.uniform(0.1, 0.4))
        likes = int(reach * random.uniform(0.02, 0.15))
        comments = int(likes * random.uniform(0.01, 0.05))
        
        posts_data.append({
            'influencer_id': influencer_id,
            'platform': platform,
            'date': date,
            'url': f"https://{platform.lower()}.com/post/{random.randint(100000, 999999)}",
            'caption': f"Check out this amazing {random.choice(brands)} product! #fitness #health",
            'reach': reach,
            'likes': likes,
            'comments': comments,
            'brand': random.choice(brands)
        })
    
    posts_df = pd.DataFrame(posts_data)
    
    # Generate tracking data (orders and revenue from posts)
    tracking_data = []
    products = ["Whey Protein", "Multivitamins", "Pre-workout", "BCAA", "Omega-3", "Protein Bars"]
    
    for _, post in posts_df.iterrows():
        # Not all posts generate orders
        if random.random() > 0.3:  # 70% chance of generating orders
            num_orders = random.randint(1, max(1, int(post['reach'] * 0.01)))  # 1% conversion rate max
            
            for _ in range(num_orders):
                tracking_data.append({
                    'source': post['platform'],
                    'campaign': f"{post['brand']}_Campaign_{random.randint(1, 10)}",
                    'influencer_id': post['influencer_id'],
                    'user_id': random.randint(100000, 999999),
                    'product': random.choice(products),
                    'brand': post['brand'],
                    'date': post['date'] + timedelta(days=random.randint(0, 7)),
                    'orders': 1,
                    'revenue': random.uniform(500, 5000)  # Revenue in INR
                })
    
    tracking_df = pd.DataFrame(tracking_data)
    
    # Generate payouts data
    payouts_data = []
    for influencer_id in range(1, len(influencer_names) + 1):
        # Some influencers paid per post, others per order
        basis = random.choice(["post", "order"])
        
        if basis == "post":
            # Count posts for this influencer
            post_count = len(posts_df[posts_df['influencer_id'] == influencer_id])
            rate = random.uniform(1000, 10000)  # Rate per post
            total_payout = post_count * rate
            orders = 0
        else:
            # Count orders for this influencer
            orders = len(tracking_df[tracking_df['influencer_id'] == influencer_id])
            rate = random.uniform(50, 200)  # Rate per order
            total_payout = orders * rate
        
        if total_payout > 0:  # Only add if there's a payout
            payouts_data.append({
                'influencer_id': influencer_id,
                'basis': basis,
                'rate': rate,
                'orders': orders,
                'total_payout': total_payout
            })
    
    payouts_df = pd.DataFrame(payouts_data)
    
    return influencers_df, posts_df, tracking_df, payouts_df

def calculate_roas_metrics(tracking_df, payouts_df):
    """Calculate ROAS and other key metrics"""
    
    # Merge tracking and payouts data
    merged_df = tracking_df.merge(
        payouts_df[['influencer_id', 'total_payout']], 
        on='influencer_id', 
        how='left'
    )
    
    # Calculate metrics by influencer
    influencer_metrics = merged_df.groupby('influencer_id').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'total_payout': 'first'
    }).reset_index()
    
    # Calculate ROAS
    influencer_metrics['roas'] = influencer_metrics['revenue'] / influencer_metrics['total_payout']
    influencer_metrics['roas'] = influencer_metrics['roas'].fillna(0)
    
    # Calculate incremental ROAS (assuming 20% baseline conversion)
    influencer_metrics['incremental_revenue'] = influencer_metrics['revenue'] * 0.8
    influencer_metrics['incremental_roas'] = influencer_metrics['incremental_revenue'] / influencer_metrics['total_payout']
    influencer_metrics['incremental_roas'] = influencer_metrics['incremental_roas'].fillna(0)
    
    return influencer_metrics

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 HealthKart Influencer Campaign Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading campaign data..."):
        influencers_df, posts_df, tracking_df, payouts_df = generate_sample_data()
        metrics_df = calculate_roas_metrics(tracking_df, payouts_df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Brand filter
    brands = ["All"] + list(tracking_df['brand'].unique())
    selected_brand = st.sidebar.selectbox("Select Brand", brands)
    
    # Platform filter
    platforms = ["All"] + list(posts_df['platform'].unique())
    selected_platform = st.sidebar.selectbox("Select Platform", platforms)
    
    # Influencer category filter
    categories = ["All"] + list(influencers_df['category'].unique())
    selected_category = st.sidebar.selectbox("Select Category", categories)
    
    # Date range filter
    min_date = posts_df['date'].min().date()
    max_date = posts_df['date'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply filters
    filtered_posts = posts_df.copy()
    filtered_tracking = tracking_df.copy()
    filtered_influencers = influencers_df.copy()
    
    if selected_brand != "All":
        filtered_posts = filtered_posts[filtered_posts['brand'] == selected_brand]
        filtered_tracking = filtered_tracking[filtered_tracking['brand'] == selected_brand]
    
    if selected_platform != "All":
        filtered_posts = filtered_posts[filtered_posts['platform'] == selected_platform]
        filtered_tracking = filtered_tracking[filtered_tracking['source'] == selected_platform]
    
    if selected_category != "All":
        category_influencers = influencers_df[influencers_df['category'] == selected_category]['id'].tolist()
        filtered_posts = filtered_posts[filtered_posts['influencer_id'].isin(category_influencers)]
        filtered_tracking = filtered_tracking[filtered_tracking['influencer_id'].isin(category_influencers)]
        filtered_influencers = filtered_influencers[filtered_influencers['category'] == selected_category]
    
    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_posts = filtered_posts[
            (filtered_posts['date'].dt.date >= start_date) & 
            (filtered_posts['date'].dt.date <= end_date)
        ]
        filtered_tracking = filtered_tracking[
            (filtered_tracking['date'].dt.date >= start_date) & 
            (filtered_tracking['date'].dt.date <= end_date)
        ]
    
    # Recalculate metrics for filtered data
    filtered_metrics = calculate_roas_metrics(filtered_tracking, payouts_df)
    
    # Key Metrics Row
    st.subheader("📈 Key Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_tracking['revenue'].sum()
        st.metric(
            label="Total Revenue",
            value=f"₹{total_revenue:,.0f}",
            delta=f"{len(filtered_tracking)} orders"
        )
    
    with col2:
        total_spend = payouts_df[payouts_df['influencer_id'].isin(filtered_tracking['influencer_id'].unique())]['total_payout'].sum()
        overall_roas = total_revenue / total_spend if total_spend > 0 else 0
        st.metric(
            label="Overall ROAS",
            value=f"{overall_roas:.2f}x",
            delta="Return on Ad Spend"
        )
    
    with col3:
        total_reach = filtered_posts['reach'].sum()
        st.metric(
            label="Total Reach",
            value=f"{total_reach:,}",
            delta=f"{len(filtered_posts)} posts"
        )
    
    with col4:
        avg_engagement = (filtered_posts['likes'] + filtered_posts['comments']).sum() / filtered_posts['reach'].sum() * 100
        st.metric(
            label="Engagement Rate",
            value=f"{avg_engagement:.2f}%",
            delta="Likes + Comments / Reach"
        )
    
    # Charts Row 1
    st.subheader("📊 Campaign Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ROAS by Influencer
        top_influencers = filtered_metrics.nlargest(10, 'roas')
        top_influencers_with_names = top_influencers.merge(
            influencers_df[['id', 'name']], 
            left_on='influencer_id', 
            right_on='id'
        )
        
        fig_roas = px.bar(
            top_influencers_with_names.head(10),
            x='name',
            y='roas',
            title='Top 10 Influencers by ROAS',
            color='roas',
            color_continuous_scale='viridis'
        )
        fig_roas.update_xaxes(tickangle=45)
        st.plotly_chart(fig_roas, use_container_width=True)
    
    with col2:
        # Revenue by Platform
        platform_revenue = filtered_tracking.groupby('source')['revenue'].sum().reset_index()
        
        fig_platform = px.pie(
            platform_revenue,
            values='revenue',
            names='source',
            title='Revenue Distribution by Platform'
        )
        st.plotly_chart(fig_platform, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Trend Over Time
        daily_revenue = filtered_tracking.groupby(filtered_tracking['date'].dt.date)['revenue'].sum().reset_index()
        daily_revenue.columns = ['date', 'revenue']
        
        fig_trend = px.line(
            daily_revenue,
            x='date',
            y='revenue',
            title='Daily Revenue Trend',
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Brand Performance
        brand_metrics = filtered_tracking.groupby('brand').agg({
            'revenue': 'sum',
            'orders': 'sum'
        }).reset_index()
        
        fig_brand = px.bar(
            brand_metrics,
            x='brand',
            y='revenue',
            title='Revenue by Brand',
            color='orders',
            color_continuous_scale='blues'
        )
        st.plotly_chart(fig_brand, use_container_width=True)
    
    # Influencer Insights Section
    st.subheader("👥 Influencer Insights")
    
    # Top Performers Table
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🏆 Top Performing Influencers**")
        top_performers = filtered_metrics.nlargest(5, 'roas')
        top_performers_display = top_performers.merge(
            influencers_df[['id', 'name', 'category', 'platform']], 
            left_on='influencer_id', 
            right_on='id'
        )[['name', 'category', 'platform', 'revenue', 'roas', 'incremental_roas']]
        
        top_performers_display['revenue'] = top_performers_display['revenue'].apply(lambda x: f"₹{x:,.0f}")
        top_performers_display['roas'] = top_performers_display['roas'].apply(lambda x: f"{x:.2f}x")
        top_performers_display['incremental_roas'] = top_performers_display['incremental_roas'].apply(lambda x: f"{x:.2f}x")
        
        st.dataframe(top_performers_display, use_container_width=True)
    
    with col2:
        st.write("**📉 Underperforming Influencers**")
        poor_performers = filtered_metrics[filtered_metrics['roas'] < 1.0].nsmallest(5, 'roas')
        if not poor_performers.empty:
            poor_performers_display = poor_performers.merge(
                influencers_df[['id', 'name', 'category', 'platform']], 
                left_on='influencer_id', 
                right_on='id'
            )[['name', 'category', 'platform', 'revenue', 'roas', 'total_payout']]
            
            poor_performers_display['revenue'] = poor_performers_display['revenue'].apply(lambda x: f"₹{x:,.0f}")
            poor_performers_display['roas'] = poor_performers_display['roas'].apply(lambda x: f"{x:.2f}x")
            poor_performers_display['total_payout'] = poor_performers_display['total_payout'].apply(lambda x: f"₹{x:,.0f}")
            
            st.dataframe(poor_performers_display, use_container_width=True)
        else:
            st.info("All influencers are performing well! 🎉")
    
    # Detailed Analytics Section
    st.subheader("📋 Detailed Campaign Data")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Posts Analytics", "Revenue Tracking", "Payout Summary", "Export Data"])
    
    with tab1:
        # Posts analytics with engagement metrics
        posts_analytics = filtered_posts.merge(
            influencers_df[['id', 'name']], 
            left_on='influencer_id', 
            right_on='id'
        )
        posts_analytics['engagement_rate'] = (posts_analytics['likes'] + posts_analytics['comments']) / posts_analytics['reach'] * 100
        posts_analytics = posts_analytics[['name', 'platform', 'brand', 'date', 'reach', 'likes', 'comments', 'engagement_rate']]
        posts_analytics['engagement_rate'] = posts_analytics['engagement_rate'].round(2)
        
        st.dataframe(posts_analytics, use_container_width=True)
    
    with tab2:
        # Revenue tracking details
        revenue_details = filtered_tracking.merge(
            influencers_df[['id', 'name']], 
            left_on='influencer_id', 
            right_on='id'
        )[['name', 'source', 'brand', 'product', 'date', 'orders', 'revenue']]
        
        st.dataframe(revenue_details, use_container_width=True)
    
    with tab3:
        # Payout summary
        payout_summary = payouts_df.merge(
            influencers_df[['id', 'name']], 
            left_on='influencer_id', 
            right_on='id'
        )[['name', 'basis', 'rate', 'orders', 'total_payout']]
        
        st.dataframe(payout_summary, use_container_width=True)
    
    with tab4:
        # Export functionality
        st.write("**📤 Export Campaign Data**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Posts Data"):
                csv = filtered_posts.to_csv(index=False)
                st.download_button(
                    label="Download Posts CSV",
                    data=csv,
                    file_name="posts_data.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("Export Revenue Data"):
                csv = filtered_tracking.to_csv(index=False)
                st.download_button(
                    label="Download Revenue CSV",
                    data=csv,
                    file_name="revenue_data.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("Export Metrics Summary"):
                summary_data = filtered_metrics.merge(
                    influencers_df[['id', 'name', 'category', 'platform']], 
                    left_on='influencer_id', 
                    right_on='id'
                )
                csv = summary_data.to_csv(index=False)
                st.download_button(
                    label="Download Metrics CSV",
                    data=csv,
                    file_name="metrics_summary.csv",
                    mime="text/csv"
                )
    
    # Key Insights Section
    st.subheader("💡 Key Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Performance Insights:**
        - Best performing platform based on ROAS
        - Top influencer categories driving revenue
        - Optimal posting frequency and timing
        - Engagement rate vs conversion correlation
        """)
        
        # Calculate actual insights
        best_platform = filtered_tracking.groupby('source')['revenue'].sum().idxmax()
        best_category = filtered_tracking.merge(
            influencers_df[['id', 'category']], 
            left_on='influencer_id', 
            right_on='id'
        ).groupby('category')['revenue'].sum().idxmax()
        
        st.info(f"🏆 **{best_platform}** is the top performing platform")
        st.info(f"🎯 **{best_category}** influencers generate highest revenue")
    
    with col2:
        st.markdown("""
        **📊 Optimization Opportunities:**
        - Reallocate budget to high-ROAS influencers
        - Focus on platforms with better conversion
        - Scale successful campaign formats
        - Review underperforming partnerships
        """)
        
        avg_roas = filtered_metrics['roas'].mean()
        high_roas_count = len(filtered_metrics[filtered_metrics['roas'] > avg_roas])
        
        st.success(f"💰 {high_roas_count} influencers performing above average ROAS")
        st.warning(f"⚠️ Consider reviewing {len(filtered_metrics) - high_roas_count} underperforming partnerships")

if __name__ == "__main__":
    main()
