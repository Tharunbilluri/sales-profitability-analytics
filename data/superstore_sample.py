import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_superstore_data(n_records=10000):
    """
    Generate realistic Superstore dataset for analysis
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Product categories and subcategories
    categories = ['Furniture', 'Office Supplies', 'Technology']
    subcategories = {
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Storage', 'Appliances', 'Art', 'Labels', 'Envelopes'],
        'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
    }
    
    # Regions and states
    regions = ['East', 'West', 'Central', 'South']
    states = {
        'East': ['New York', 'Pennsylvania', 'Massachusetts', 'Connecticut', 'New Jersey'],
        'West': ['California', 'Washington', 'Oregon', 'Nevada', 'Arizona'],
        'Central': ['Illinois', 'Ohio', 'Michigan', 'Indiana', 'Wisconsin'],
        'South': ['Texas', 'Florida', 'Georgia', 'North Carolina', 'Virginia']
    }
    
    # Ship modes
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    
    # Customer segments
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    # Generate data
    data = []
    
    for i in range(n_records):
        # Random date in 2022-2023
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2023, 12, 31)
        random_days = random.randint(0, (end_date - start_date).days)
        order_date = start_date + timedelta(days=random_days)
        
        # Random category and subcategory
        category = random.choice(categories)
        subcategory = random.choice(subcategories[category])
        
        # Random region and state
        region = random.choice(regions)
        state = random.choice(states[region])
        
        # Random ship mode and segment
        ship_mode = random.choice(ship_modes)
        segment = random.choice(segments)
        
        # Generate realistic product names
        product_names = {
            'Chairs': ['Office Chair', 'Ergonomic Chair', 'Conference Chair', 'Guest Chair'],
            'Tables': ['Office Table', 'Conference Table', 'Coffee Table', 'Dining Table'],
            'Bookcases': ['3-Shelf Bookcase', '5-Shelf Bookcase', 'Corner Bookcase'],
            'Furnishings': ['Table Lamp', 'Floor Lamp', 'Wall Art', 'Rug'],
            'Paper': ['Copy Paper', 'Notebook Paper', 'Cardstock', 'Envelopes'],
            'Binders': ['3-Ring Binder', '5-Ring Binder', 'Binder Clips', 'Binder Dividers'],
            'Storage': ['File Cabinet', 'Storage Box', 'Desk Organizer', 'Filing Tray'],
            'Appliances': ['Desk Fan', 'Space Heater', 'Coffee Maker', 'Mini Fridge'],
            'Art': ['Markers', 'Pencils', 'Pens', 'Highlighters'],
            'Labels': ['Address Labels', 'File Labels', 'Price Labels', 'Shipping Labels'],
            'Envelopes': ['Business Envelopes', 'Shipping Envelopes', 'Greeting Card Envelopes'],
            'Phones': ['Smartphone', 'Landline Phone', 'Cordless Phone', 'Conference Phone'],
            'Accessories': ['Phone Case', 'Charger', 'Headphones', 'Bluetooth Speaker'],
            'Machines': ['Printer', 'Scanner', 'Fax Machine', 'Projector'],
            'Copiers': ['Desktop Copier', 'Floor Copier', 'Color Copier', 'Multifunction Copier']
        }
        
        product_name = random.choice(product_names[subcategory])
        
        # Generate realistic pricing
        base_prices = {
            'Furniture': (50, 500),
            'Office Supplies': (5, 100),
            'Technology': (25, 1000)
        }
        
        min_price, max_price = base_prices[category]
        unit_price = round(random.uniform(min_price, max_price), 2)
        
        # Quantity (1-10)
        quantity = random.randint(1, 10)
        
        # Sales and profit calculations
        sales = unit_price * quantity
        
        # Profit margin varies by category
        margin_ranges = {
            'Furniture': (0.15, 0.35),
            'Office Supplies': (0.20, 0.40),
            'Technology': (0.10, 0.30)
        }
        
        min_margin, max_margin = margin_ranges[category]
        profit_margin = random.uniform(min_margin, max_margin)
        profit = sales * profit_margin
        
        # Discount (0-30%)
        discount = random.uniform(0, 0.30)
        discounted_sales = sales * (1 - discount)
        
        # Shipping cost based on ship mode
        shipping_costs = {
            'Standard Class': (5, 15),
            'Second Class': (8, 20),
            'First Class': (12, 25),
            'Same Day': (25, 50)
        }
        
        min_shipping, max_shipping = shipping_costs[ship_mode]
        shipping_cost = random.uniform(min_shipping, max_shipping)
        
        # Customer ID (consistent for same customer)
        customer_id = f"CUST_{random.randint(1000, 9999)}"
        
        # Order ID
        order_id = f"ORD_{random.randint(10000, 99999)}"
        
        # Product ID
        product_id = f"PROD_{random.randint(1000, 9999)}"
        
        data.append({
            'Row ID': i + 1,
            'Order ID': order_id,
            'Order Date': order_date,
            'Ship Date': order_date + timedelta(days=random.randint(1, 14)),
            'Ship Mode': ship_mode,
            'Customer ID': customer_id,
            'Customer Name': f"Customer {customer_id}",
            'Segment': segment,
            'Country': 'United States',
            'City': f"City {random.randint(1, 50)}",
            'State': state,
            'Postal Code': random.randint(10000, 99999),
            'Region': region,
            'Product ID': product_id,
            'Category': category,
            'Sub-Category': subcategory,
            'Product Name': product_name,
            'Sales': round(sales, 2),
            'Quantity': quantity,
            'Discount': round(discount, 3),
            'Profit': round(profit, 2),
            'Unit Price': unit_price,
            'Shipping Cost': round(shipping_cost, 2)
        })
    
    df = pd.DataFrame(data)
    
    # Add some seasonal patterns
    df['Month'] = df['Order Date'].dt.month
    df['Quarter'] = df['Order Date'].dt.quarter
    df['Year'] = df['Order Date'].dt.year
    
    # Add some realistic correlations
    # Higher sales in Q4 (holiday season)
    q4_mask = df['Quarter'] == 4
    df.loc[q4_mask, 'Sales'] = df.loc[q4_mask, 'Sales'] * 1.3
    df.loc[q4_mask, 'Profit'] = df.loc[q4_mask, 'Profit'] * 1.2
    
    # Technology has higher sales in Q1 (new year purchases)
    q1_tech_mask = (df['Quarter'] == 1) & (df['Category'] == 'Technology')
    df.loc[q1_tech_mask, 'Sales'] = df.loc[q1_tech_mask, 'Sales'] * 1.2
    
    return df

if __name__ == "__main__":
    # Generate dataset
    df = generate_superstore_data(15000)
    
    # Save to CSV
    df.to_csv('data/superstore.csv', index=False)
    
    # Save to Excel for easier viewing
    with pd.ExcelWriter('data/superstore.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
        
        # Create summary sheet
        summary_data = {
            'Metric': ['Total Records', 'Total Sales', 'Total Profit', 'Total Customers', 'Date Range'],
            'Value': [
                len(df),
                f"${df['Sales'].sum():,.2f}",
                f"${df['Profit'].sum():,.2f}",
                df['Customer ID'].nunique(),
                f"{df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    print("Superstore dataset generated successfully!")
    print(f"Total records: {len(df):,}")
    print(f"Total sales: ${df['Sales'].sum():,.2f}")
    print(f"Total profit: ${df['Profit'].sum():,.2f}")
    print(f"Total customers: {df['Customer ID'].nunique():,}")
    print(f"Date range: {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")
    print("\nFiles saved:")
    print("- data/superstore.csv")
    print("- data/superstore.xlsx")
