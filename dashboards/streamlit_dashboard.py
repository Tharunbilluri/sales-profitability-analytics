#!/usr/bin/env python3
"""
Interactive Sales & Profitability Dashboard
Built with Streamlit for real-time business insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Sales & Profitability Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
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
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 6px solid #ffd700;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .insight-box h4 {
        color: #ffd700;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .insight-box ul, .insight-box ol {
        color: white;
        font-weight: 500;
    }
    .insight-box li {
        margin: 0.5rem 0;
        padding: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the superstore dataset"""
    try:
        df = pd.read_csv('data/superstore.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
        df['Month'] = df['Order Date'].dt.month
        df['Quarter'] = df['Order Date'].dt.quarter
        df['Year'] = df['Order Date'].dt.year
        df['Month_Name'] = df['Order Date'].dt.strftime('%b')
        df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please run the data generation script first.")
        return None

def create_kpi_metrics(df):
    """Create KPI metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['Sales'].sum()
        st.metric(
            label="Total Sales",
            value=f"₹{total_sales*83:,.0f}",
            delta=f"₹{total_sales*83/len(df):.0f} avg per order"
        )
    
    with col2:
        total_profit = df['Profit'].sum()
        st.metric(
            label="Total Profit",
            value=f"₹{total_profit*83:,.0f}",
            delta=f"{(total_profit/total_sales*100):.1f}% margin"
        )
    
    with col3:
        total_customers = df['Customer ID'].nunique()
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}",
            delta=f"{df['Order ID'].nunique()/total_customers:.1f} orders per customer"
        )
    
    with col4:
        total_products = df['Product ID'].nunique()
        st.metric(
            label="Total Products",
            value=f"{total_products:,}",
            delta=f"{df['Quantity'].sum()/total_products:.0f} units per product"
        )

def create_sales_overview_chart(df):
    """Create sales overview chart"""
    st.subheader("📈 Sales Overview")
    
    # Monthly sales trend
    monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    monthly_sales['Date'] = pd.to_datetime(monthly_sales[['Year', 'Month']].assign(day=1))
    
    fig = px.line(
        monthly_sales, 
        x='Date', 
        y='Sales',
        title='Monthly Sales Trend',
        markers=True,
        line_shape='linear'
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales (₹)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def create_category_analysis(df):
    """Create category analysis charts"""
    st.subheader("🏷️ Category Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by category
        category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
        fig = px.bar(
            x=category_sales.values,
            y=category_sales.index,
            orientation='h',
            title='Sales by Category (₹)',
            color=category_sales.values,
            color_continuous_scale='blues'
        )
        fig.update_layout(
            xaxis_title="Sales (₹)",
            yaxis_title="Category",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit margin by category
        category_margin = df.groupby('Category')['Profit_Margin'].mean().sort_values(ascending=True)
        fig = px.bar(
            x=category_margin.values,
            y=category_margin.index,
            orientation='h',
            title='Average Profit Margin by Category',
            color=category_margin.values,
            color_continuous_scale='greens'
        )
        fig.update_layout(
            xaxis_title="Profit Margin (%)",
            yaxis_title="Category",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def create_regional_analysis(df):
    """Create regional analysis charts"""
    st.subheader("🌍 Regional Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by region
        regional_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=True)
        fig = px.bar(
            x=regional_sales.values,
            y=regional_sales.index,
            orientation='h',
            title='Sales by Region (₹)',
            color=regional_sales.values,
            color_continuous_scale='reds'
        )
        fig.update_layout(
            xaxis_title="Sales (₹)",
            yaxis_title="Region",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional profit margins
        regional_margin = df.groupby('Region')['Profit_Margin'].mean().sort_values(ascending=True)
        fig = px.bar(
            x=regional_margin.values,
            y=regional_margin.index,
            orientation='h',
            title='Profit Margin by Region',
            color=regional_margin.values,
            color_continuous_scale='purples'
        )
        fig.update_layout(
            xaxis_title="Profit Margin (%)",
            yaxis_title="Region",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def create_customer_analysis(df):
    """Create customer analysis charts"""
    st.subheader("👥 Customer Segment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by customer segment
        segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=True)
        fig = px.bar(
            x=segment_sales.values,
            y=segment_sales.index,
            orientation='h',
            title='Sales by Customer Segment (₹)',
            color=segment_sales.values,
            color_continuous_scale='oranges'
        )
        fig.update_layout(
            xaxis_title="Sales (₹)",
            yaxis_title="Segment",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer segment profit margins
        segment_margin = df.groupby('Segment')['Profit_Margin'].mean().sort_values(ascending=True)
        fig = px.bar(
            x=segment_margin.values,
            y=segment_margin.index,
            orientation='h',
            title='Profit Margin by Customer Segment',
            color=segment_margin.values,
            color_continuous_scale='teal'
        )
        fig.update_layout(
            xaxis_title="Profit Margin (%)",
            yaxis_title="Segment",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def create_product_analysis(df):
    """Create product analysis charts"""
    st.subheader("📦 Product Performance Analysis")
    
    # Top products by sales
    top_products_sales = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=top_products_sales.values,
        y=top_products_sales.index,
        orientation='h',
        title='Top 10 Products by Sales (₹)',
        color=top_products_sales.values,
        color_continuous_scale='viridis'
    )
    fig.update_layout(
        xaxis_title="Sales (₹)",
        yaxis_title="Product",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top products by profit
    col1, col2 = st.columns(2)
    
    with col1:
        top_products_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=top_products_profit.values,
            y=top_products_profit.index,
            orientation='h',
            title='Top 10 Products by Profit (₹)',
            color=top_products_profit.values,
            color_continuous_scale='plasma'
        )
        fig.update_layout(
            xaxis_title="Profit (₹)",
            yaxis_title="Product",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # High margin products
        high_margin_products = df[df['Sales'] > 1000].groupby('Product Name')['Profit_Margin'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=high_margin_products.values,
            y=high_margin_products.index,
            orientation='h',
            title='Top 10 Products by Profit Margin',
            color=high_margin_products.values,
            color_continuous_scale='inferno'
        )
        fig.update_layout(
            xaxis_title="Profit Margin (%)",
            yaxis_title="Product",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def create_discount_analysis(df):
    """Create discount impact analysis"""
    st.subheader("🎯 Discount Impact Analysis")
    
    # Create discount buckets
    df['Discount_Bucket'] = pd.cut(
        df['Discount'], 
        bins=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, float('inf')],
        labels=['0-5%', '5-10%', '10-15%', '15-20%', '20-25%', '25-30%', '30%+']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Discount vs profit margin
        discount_impact = df.groupby('Discount_Bucket').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        discount_impact['Profit_Margin'] = (discount_impact['Profit'] / discount_impact['Sales'] * 100).round(2)
        
        fig = px.bar(
            x=discount_impact['Discount_Bucket'],
            y=discount_impact['Profit_Margin'],
            title='Profit Margin by Discount Level',
            color=discount_impact['Profit_Margin'],
            color_continuous_scale='rdylgn'
        )
        fig.update_layout(
            xaxis_title="Discount Level",
            yaxis_title="Profit Margin (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Discount vs sales scatter
        sample_data = df.sample(n=1000)  # Sample for better visualization
        fig = px.scatter(
            sample_data,
            x='Discount',
            y='Profit',
            color='Category',
            title='Discount vs Profit Impact',
            size='Sales',
            hover_data=['Product Name', 'Region']
        )
        fig.update_layout(
            xaxis_title="Discount Rate",
            yaxis_title="Profit (₹)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def create_seasonal_analysis(df):
    """Create seasonal trends analysis"""
    st.subheader("📅 Seasonal Trends Analysis")
    
    # Quarterly trends
    quarterly_data = df.groupby(['Year', 'Quarter']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    quarterly_data['Quarter_Name'] = 'Q' + quarterly_data['Quarter'].astype(str) + ' ' + quarterly_data['Year'].astype(str)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Quarterly Sales Trend', 'Quarterly Profit Trend'),
        vertical_spacing=0.1
    )
    
    # Sales trend
    fig.add_trace(
        go.Bar(x=quarterly_data['Quarter_Name'], y=quarterly_data['Sales'], name='Sales', marker_color='skyblue'),
        row=1, col=1
    )
    
    # Profit trend
    fig.add_trace(
        go.Bar(x=quarterly_data['Quarter_Name'], y=quarterly_data['Profit'], name='Profit', marker_color='lightgreen'),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def create_insights_panel(df):
    """Create business insights panel"""
    st.subheader("💡 Business Insights & Recommendations")
    st.info("💱 **Currency**: All amounts shown in Indian Rupees (₹) | Exchange Rate: 1 USD = ₹83")
    
    # Calculate key insights
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    overall_margin = (total_profit / total_sales * 100)
    
    best_category = df.groupby('Category')['Sales'].sum().idxmax()
    best_category_sales = df.groupby('Category')['Sales'].sum().max()
    
    best_region = df.groupby('Region')['Sales'].sum().idxmax()
    best_region_sales = df.groupby('Region')['Sales'].sum().max()
    
    best_segment = df.groupby('Segment')['Sales'].sum().idxmax()
    best_segment_sales = df.groupby('Segment')['Sales'].sum().max()
    
    # Display insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>🏆 Top Performers</h4>
        <ul>
        <li><strong>Best Category:</strong> {} (₹{:,.0f})</li>
        <li><strong>Best Region:</strong> {} (₹{:,.0f})</li>
        <li><strong>Best Segment:</strong> {} (₹{:,.0f})</li>
        </ul>
        </div>
        """.format(best_category, best_category_sales*83, best_region, best_region_sales*83, best_segment, best_segment_sales*83), 
        unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>💰 Financial Overview</h4>
        <ul>
        <li><strong>Overall Margin:</strong> {:.1f}%</li>
        <li><strong>Total Customers:</strong> {:,}</li>
        <li><strong>Total Products:</strong> {:,}</li>
        </ul>
        </div>
        """.format(overall_margin, df['Customer ID'].nunique(), df['Product ID'].nunique()), 
        unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("""
    <div class="insight-box">
    <h4>🚀 Strategic Recommendations</h4>
    <ol>
    <li><strong>Focus on High-Margin Products:</strong> Prioritize products with profit margins above 20%</li>
    <li><strong>Seasonal Planning:</strong> Stock up before peak seasons (Q4 for general, Q1 for Technology)</li>
    <li><strong>Discount Optimization:</strong> Limit discounts to 15-20% range to maintain profitability</li>
    <li><strong>Regional Expansion:</strong> Focus marketing efforts on underperforming regions</li>
    <li><strong>Customer Retention:</strong> Implement loyalty programs for high-value segments</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">📊 Sales & Profitability Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### 🇮🇳 E-commerce Business Intelligence Dashboard (Indian Market)")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Category filter
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )
    
    # Region filter
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[df['Order Date'].min(), df['Order Date'].max()],
        min_value=df['Order Date'].min(),
        max_value=df['Order Date'].max()
    )
    
    # Apply filters
    if selected_categories:
        df = df[df['Category'].isin(selected_categories)]
    if selected_regions:
        df = df[df['Region'].isin(selected_regions)]
    if len(date_range) == 2:
        df = df[(df['Order Date'].dt.date >= date_range[0]) & (df['Order Date'].dt.date <= date_range[1])]
    
    # Display filtered data info
    st.sidebar.markdown(f"**Filtered Records:** {len(df):,}")
    st.sidebar.markdown(f"**Date Range:** {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")
    
    # Main dashboard content
    create_kpi_metrics(df)
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Sales Overview", "🏷️ Categories", "🌍 Regions", "👥 Customers", 
        "📦 Products", "🎯 Discounts", "📅 Seasonal"
    ])
    
    with tab1:
        create_sales_overview_chart(df)
    
    with tab2:
        create_category_analysis(df)
    
    with tab3:
        create_regional_analysis(df)
    
    with tab4:
        create_customer_analysis(df)
    
    with tab5:
        create_product_analysis(df)
    
    with tab6:
        create_discount_analysis(df)
    
    with tab7:
        create_seasonal_analysis(df)
    
    # Business insights
    create_insights_panel(df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>📊 Sales & Profitability Analytics Dashboard | Built with Streamlit</p>
    <p>Data-driven insights for business decision making</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
