#!/usr/bin/env python3
"""
Sales & Profitability Analysis Script
Comprehensive analysis of Superstore dataset for business insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SalesAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with data"""
        self.df = pd.read_csv(data_path)
        self.df['Order Date'] = pd.to_datetime(self.df['Order Date'])
        self.df['Ship Date'] = pd.to_datetime(self.df['Ship Date'])
        self.df['Month'] = self.df['Order Date'].dt.month
        self.df['Quarter'] = self.df['Order Date'].dt.quarter
        self.df['Year'] = self.df['Order Date'].dt.year
        self.df['Month_Name'] = self.df['Order Date'].dt.strftime('%b')
        
        # Calculate additional metrics
        self.df['Profit_Margin'] = (self.df['Profit'] / self.df['Sales'] * 100).round(2)
        self.df['Discount_Impact'] = self.df['Sales'] * self.df['Discount']
        
        print(f"Dataset loaded: {len(self.df):,} records")
        print(f"Date range: {self.df['Order Date'].min().strftime('%Y-%m-%d')} to {self.df['Order Date'].max().strftime('%Y-%m-%d')}")
    
    def generate_summary_statistics(self):
        """Generate comprehensive summary statistics"""
        print("=" * 60)
        print("SALES & PROFITABILITY SUMMARY STATISTICS")
        print("=" * 60)
        
        # Overall metrics
        total_sales = self.df['Sales'].sum()
        total_profit = self.df['Profit'].sum()
        total_customers = self.df['Customer ID'].nunique()
        total_products = self.df['Product ID'].nunique()
        
        print(f"Total Sales: ${total_sales:,.2f}")
        print(f"Total Profit: ${total_profit:,.2f}")
        print(f"Overall Profit Margin: {(total_profit/total_sales*100):.2f}%")
        print(f"Total Customers: {total_customers:,}")
        print(f"Total Products: {total_products:,}")
        print(f"Total Orders: {self.df['Order ID'].nunique():,}")
        
        # Category breakdown
        print("\n" + "=" * 40)
        print("CATEGORY PERFORMANCE")
        print("=" * 40)
        
        category_summary = self.df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Order ID': 'nunique'
        }).round(2)
        
        category_summary['Profit_Margin'] = (category_summary['Profit'] / category_summary['Sales'] * 100).round(2)
        category_summary['Avg_Order_Value'] = (category_summary['Sales'] / category_summary['Order ID']).round(2)
        category_summary = category_summary.sort_values('Sales', ascending=False)
        
        print(category_summary)
        
        return category_summary
    
    def analyze_top_products(self, top_n=10):
        """Analyze top performing products"""
        print("\n" + "=" * 50)
        print(f"TOP {top_n} PRODUCTS ANALYSIS")
        print("=" * 50)
        
        # Top products by sales
        top_sales = self.df.groupby('Product Name').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum',
            'Order ID': 'nunique'
        }).round(2)
        
        top_sales['Profit_Margin'] = (top_sales['Profit'] / top_sales['Sales'] * 100).round(2)
        top_sales['Avg_Order_Value'] = (top_sales['Sales'] / top_sales['Order ID']).round(2)
        
        print("Top Products by Sales:")
        print(top_sales.sort_values('Sales', ascending=False).head(top_n))
        
        print("\nTop Products by Profit:")
        print(top_sales.sort_values('Profit', ascending=False).head(top_n))
        
        print("\nTop Products by Profit Margin:")
        print(top_sales[top_sales['Sales'] > 1000].sort_values('Profit_Margin', ascending=False).head(top_n))
        
        return top_sales
    
    def analyze_seasonal_trends(self):
        """Analyze seasonal sales patterns"""
        print("\n" + "=" * 50)
        print("SEASONAL TRENDS ANALYSIS")
        print("=" * 50)
        
        # Monthly trends
        monthly_trends = self.df.groupby(['Year', 'Month', 'Month_Name']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        
        monthly_trends['Profit_Margin'] = (monthly_trends['Profit'] / monthly_trends['Sales'] * 100).round(2)
        monthly_trends = monthly_trends.sort_values(['Year', 'Month'])
        
        print("Monthly Sales Trends:")
        print(monthly_trends)
        
        # Quarterly trends
        quarterly_trends = self.df.groupby(['Year', 'Quarter']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        
        quarterly_trends['Profit_Margin'] = (quarterly_trends['Profit'] / quarterly_trends['Sales'] * 100).round(2)
        quarterly_trends['Quarter_Name'] = 'Q' + quarterly_trends['Quarter'].astype(str) + ' ' + quarterly_trends['Year'].astype(str)
        
        print("\nQuarterly Sales Trends:")
        print(quarterly_trends)
        
        # Seasonal patterns by category
        seasonal_category = self.df.groupby(['Category', 'Quarter']).agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        seasonal_category['Profit_Margin'] = (seasonal_category['Profit'] / seasonal_category['Sales'] * 100).round(2)
        
        print("\nSeasonal Patterns by Category:")
        print(seasonal_category)
        
        return monthly_trends, quarterly_trends, seasonal_category
    
    def analyze_regional_performance(self):
        """Analyze performance by region and state"""
        print("\n" + "=" * 50)
        print("REGIONAL PERFORMANCE ANALYSIS")
        print("=" * 50)
        
        # Regional performance
        regional_perf = self.df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique',
            'Customer ID': 'nunique'
        }).round(2)
        
        regional_perf['Profit_Margin'] = (regional_perf['Profit'] / regional_perf['Sales'] * 100).round(2)
        regional_perf['Avg_Order_Value'] = (regional_perf['Sales'] / regional_perf['Order ID']).round(2)
        regional_perf['Customers_per_Order'] = (regional_perf['Customer ID'] / regional_perf['Order ID']).round(2)
        
        print("Regional Performance:")
        print(regional_perf.sort_values('Sales', ascending=False))
        
        # State performance
        state_perf = self.df.groupby('State').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).round(2)
        
        state_perf['Profit_Margin'] = (state_perf['Profit'] / state_perf['Sales'] * 100).round(2)
        state_perf['Avg_Order_Value'] = (state_perf['Sales'] / state_perf['Order ID']).round(2)
        
        print("\nTop 10 States by Sales:")
        print(state_perf.sort_values('Sales', ascending=False).head(10))
        
        return regional_perf, state_perf
    
    def analyze_customer_segments(self):
        """Analyze customer segments and profitability"""
        print("\n" + "=" * 50)
        print("CUSTOMER SEGMENT ANALYSIS")
        print("=" * 50)
        
        # Segment performance
        segment_perf = self.df.groupby('Segment').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique',
            'Customer ID': 'nunique'
        }).round(2)
        
        segment_perf['Profit_Margin'] = (segment_perf['Profit'] / segment_perf['Sales'] * 100).round(2)
        segment_perf['Avg_Order_Value'] = (segment_perf['Sales'] / segment_perf['Order ID']).round(2)
        segment_perf['Orders_per_Customer'] = (segment_perf['Order ID'] / segment_perf['Customer ID']).round(2)
        
        print("Customer Segment Performance:")
        print(segment_perf)
        
        # Customer lifetime value analysis
        customer_lifetime = self.df.groupby('Customer ID').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique',
            'Order Date': ['min', 'max']
        }).round(2)
        
        customer_lifetime.columns = ['Total_Sales', 'Total_Profit', 'Total_Orders', 'First_Order', 'Last_Order']
        customer_lifetime['Customer_Lifetime_Days'] = (customer_lifetime['Last_Order'] - customer_lifetime['First_Order']).dt.days
        customer_lifetime['Avg_Order_Value'] = (customer_lifetime['Total_Sales'] / customer_lifetime['Total_Orders']).round(2)
        customer_lifetime['Profit_Margin'] = (customer_lifetime['Total_Profit'] / customer_lifetime['Total_Sales'] * 100).round(2)
        
        print("\nCustomer Lifetime Value Summary:")
        print(customer_lifetime.describe())
        
        return segment_perf, customer_lifetime
    
    def analyze_discount_impact(self):
        """Analyze the impact of discounts on profitability"""
        print("\n" + "=" * 50)
        print("DISCOUNT IMPACT ANALYSIS")
        print("=" * 50)
        
        # Create discount buckets
        self.df['Discount_Bucket'] = pd.cut(self.df['Discount'], 
                                           bins=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, float('inf')],
                                           labels=['0-5%', '5-10%', '10-15%', '15-20%', '20-25%', '25-30%', '30%+'])
        
        discount_impact = self.df.groupby('Discount_Bucket').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).round(2)
        
        discount_impact['Profit_Margin'] = (discount_impact['Profit'] / discount_impact['Sales'] * 100).round(2)
        discount_impact['Avg_Order_Value'] = (discount_impact['Sales'] / discount_impact['Order ID']).round(2)
        
        print("Discount Impact Analysis:")
        print(discount_impact)
        
        # Correlation analysis
        correlation = self.df['Discount'].corr(self.df['Profit'])
        print(f"\nCorrelation between Discount and Profit: {correlation:.4f}")
        
        # Category-wise discount analysis
        category_discount = self.df.groupby(['Category', 'Discount_Bucket']).agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        category_discount['Profit_Margin'] = (category_discount['Profit'] / category_discount['Sales'] * 100).round(2)
        
        print("\nDiscount Analysis by Category:")
        print(category_discount)
        
        return discount_impact, category_discount
    
    def generate_insights_report(self):
        """Generate comprehensive business insights report"""
        print("\n" + "=" * 80)
        print("BUSINESS INSIGHTS & RECOMMENDATIONS")
        print("=" * 80)
        
        # Get all analysis results
        category_summary = self.generate_summary_statistics()
        top_products = self.analyze_top_products()
        monthly_trends, quarterly_trends, seasonal_category = self.analyze_seasonal_trends()
        regional_perf, state_perf = self.analyze_regional_performance()
        segment_perf, customer_lifetime = self.analyze_customer_segments()
        discount_impact, category_discount = self.analyze_discount_impact()
        
        # Generate insights
        insights = []
        
        # Top performing category
        best_category = category_summary.loc[category_summary['Sales'].idxmax()]
        insights.append(f"🏆 {best_category.name} is the top-performing category with ${best_category['Sales']:,.2f} in sales and {best_category['Profit_Margin']:.2f}% profit margin")
        
        # Best profit margin category
        best_margin_category = category_summary.loc[category_summary['Profit_Margin'].idxmax()]
        insights.append(f"💰 {best_margin_category.name} has the best profit margin at {best_margin_category['Profit_Margin']:.2f}%")
        
        # Regional insights
        best_region = regional_perf.loc[regional_perf['Sales'].idxmax()]
        insights.append(f"🌍 {best_region.name} is the top-performing region with ${best_region['Sales']:,.2f} in sales")
        
        # Customer segment insights
        best_segment = segment_perf.loc[segment_perf['Sales'].idxmax()]
        insights.append(f"👥 {best_segment.name} customers generate the highest sales at ${best_segment['Sales']:,.2f}")
        
        # Seasonal insights
        best_quarter = quarterly_trends.loc[quarterly_trends['Sales'].idxmax()]
        insights.append(f"📅 {best_quarter['Quarter_Name']} shows the highest sales at ${best_quarter['Sales']:,.2f}")
        
        # Discount insights
        optimal_discount = discount_impact.loc[discount_impact['Profit_Margin'].idxmax()]
        insights.append(f"🎯 Optimal discount range appears to be {optimal_discount.name} with {optimal_discount['Profit_Margin']:.2f}% profit margin")
        
        print("\n".join(insights))
        
        # Recommendations
        print("\n" + "=" * 50)
        print("STRATEGIC RECOMMENDATIONS")
        print("=" * 50)
        
        recommendations = [
            "🚀 **Focus on High-Margin Products**: Prioritize products in categories with profit margins above 20%",
            "📈 **Seasonal Planning**: Stock up on high-demand products before peak seasons (Q4 for general, Q1 for Technology)",
            "🎯 **Discount Optimization**: Limit discounts to 15-20% range to maintain profitability",
            "🌍 **Regional Expansion**: Focus marketing efforts on underperforming regions to drive growth",
            "👥 **Customer Retention**: Implement loyalty programs for high-value customer segments",
            "📊 **Inventory Management**: Use seasonal trends to optimize stock levels and reduce carrying costs"
        ]
        
        for rec in recommendations:
            print(rec)
        
        return insights, recommendations
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("\nCreating visualizations...")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Sales by Category
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        
        # Category sales
        category_sales = self.df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
        axes[0,0].barh(category_sales.index, category_sales.values, color='skyblue')
        axes[0,0].set_title('Total Sales by Category', fontsize=14, fontweight='bold')
        axes[0,0].set_xlabel('Sales ($)')
        
        # Monthly trends
        monthly_sales = self.df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
        monthly_sales['Date'] = pd.to_datetime(monthly_sales[['Year', 'Month']].assign(day=1))
        axes[0,1].plot(monthly_sales['Date'], monthly_sales['Sales'], marker='o', linewidth=2, color='green')
        axes[0,1].set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
        axes[0,1].set_xlabel('Date')
        axes[0,1].set_ylabel('Sales ($)')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Regional performance
        regional_sales = self.df.groupby('Region')['Sales'].sum().sort_values(ascending=True)
        axes[1,0].barh(regional_sales.index, regional_sales.values, color='lightcoral')
        axes[1,0].set_title('Sales by Region', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('Sales ($)')
        
        # Customer segments
        segment_sales = self.df.groupby('Segment')['Sales'].sum().sort_values(ascending=True)
        axes[1,1].barh(segment_sales.index, segment_sales.values, color='lightgreen')
        axes[1,1].set_title('Sales by Customer Segment', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('Sales ($)')
        
        plt.tight_layout()
        plt.savefig('dashboards/sales_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Profitability Analysis
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        
        # Profit margin by category
        category_margin = self.df.groupby('Category')['Profit_Margin'].mean().sort_values(ascending=True)
        axes[0,0].barh(category_margin.index, category_margin.values, color='gold')
        axes[0,0].set_title('Average Profit Margin by Category', fontsize=14, fontweight='bold')
        axes[0,0].set_xlabel('Profit Margin (%)')
        
        # Discount vs Profit scatter
        sample_data = self.df.sample(n=1000)  # Sample for better visualization
        axes[0,1].scatter(sample_data['Discount'], sample_data['Profit'], alpha=0.6, color='purple')
        axes[0,1].set_title('Discount vs Profit Impact', fontsize=14, fontweight='bold')
        axes[0,1].set_xlabel('Discount Rate')
        axes[0,1].set_ylabel('Profit ($)')
        
        # Seasonal profit trends
        quarterly_profit = self.df.groupby(['Year', 'Quarter'])['Profit'].sum().reset_index()
        quarterly_profit['Quarter_Name'] = 'Q' + quarterly_profit['Quarter'].astype(str) + ' ' + quarterly_profit['Year'].astype(str)
        axes[1,0].bar(range(len(quarterly_profit)), quarterly_profit['Profit'], color='orange')
        axes[1,0].set_title('Quarterly Profit Trends', fontsize=14, fontweight='bold')
        axes[1,0].set_xlabel('Quarter')
        axes[1,0].set_ylabel('Profit ($)')
        axes[1,0].set_xticks(range(len(quarterly_profit)))
        axes[1,0].set_xticklabels(quarterly_profit['Quarter_Name'], rotation=45)
        
        # Top products by profit
        top_profit_products = self.df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
        axes[1,1].barh(range(len(top_profit_products)), top_profit_products.values, color='lightblue')
        axes[1,1].set_title('Top 10 Products by Profit', fontsize=14, fontweight='bold')
        axes[1,1].set_xlabel('Profit ($)')
        axes[1,1].set_yticks(range(len(top_profit_products)))
        axes[1,1].set_yticklabels(top_profit_products.index, fontsize=8)
        
        plt.tight_layout()
        plt.savefig('dashboards/profitability_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualizations saved to dashboards/ folder")
        
        return True

def main():
    """Main execution function"""
    print("Sales & Profitability Analytics")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = SalesAnalyzer('data/superstore.csv')
    
    # Generate comprehensive analysis
    insights, recommendations = analyzer.generate_insights_report()
    
    # Create visualizations
    analyzer.create_visualizations()
    
    print("\nAnalysis complete! Check the dashboards/ folder for visualizations.")

if __name__ == "__main__":
    main()
