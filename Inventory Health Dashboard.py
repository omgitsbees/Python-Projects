import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import ipywidgets as widgets
from IPython.display import display

def generate_inventory_dashboard():
    # Expanded Sample Data
    np.random.seed(42)
    warehouses = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    num_warehouses = len(warehouses)
    
    data = {
        'Warehouse': np.random.choice(warehouses, 100),
        'Inventory_Turnover': np.random.uniform(1.5, 12, 100),
        'Stockout_Rate': np.random.uniform(0, 20, 100),
        'Order_Fulfillment_Time': np.random.uniform(12, 96, 100),
        'Safety_Incidents': np.random.randint(0, 15, 100),
        'On_Time_Delivery': np.random.uniform(75, 100, 100),
        'Order_Accuracy': np.random.uniform(80, 100, 100),
        'Carrying_Cost': np.random.uniform(3, 25, 100),
        'Warehouse_Utilization': np.random.uniform(45, 98, 100),
        'Order_Picking_Accuracy': np.random.uniform(85, 99, 100),
        'Lost_Sales': np.random.uniform(5000, 50000, 100),
        'Return_Rate': np.random.uniform(0, 10, 100),
        'Backorder_Rate': np.random.uniform(0, 15, 100)
    }
    
    df = pd.DataFrame(data)
    
    # Display Data
    print(df)
    
    # Filters
    warehouse_filter = widgets.Dropdown(
        options=['All'] + list(set(df['Warehouse'])),
        value='All',
        description='Warehouse:'
    )
    
    def update_dashboard(warehouse):
        filtered_df = df if warehouse == 'All' else df[df['Warehouse'] == warehouse]
        
        plt.figure(figsize=(15, 8))
        
        plt.subplot(2, 3, 1)
        sns.barplot(x='Warehouse', y='Inventory_Turnover', data=filtered_df, palette='viridis')
        plt.title('Inventory Turnover')
        plt.ylabel('Turnover Ratio')
        
        plt.subplot(2, 3, 2)
        sns.barplot(x='Warehouse', y='Stockout_Rate', data=filtered_df, palette='coolwarm')
        plt.title('Stockout Rate')
        plt.ylabel('Stockout Rate (%)')
        
        plt.subplot(2, 3, 3)
        sns.barplot(x='Warehouse', y='On_Time_Delivery', data=filtered_df, palette='Blues')
        plt.title('On-Time Delivery')
        plt.ylabel('Percentage (%)')
        
        plt.subplot(2, 3, 4)
        sns.barplot(x='Warehouse', y='Lost_Sales', data=filtered_df, palette='Oranges')
        plt.title('Lost Sales')
        plt.ylabel('Amount ($)')
        
        plt.subplot(2, 3, 5)
        sns.barplot(x='Warehouse', y='Return_Rate', data=filtered_df, palette='Purples')
        plt.title('Return Rate')
        plt.ylabel('Percentage (%)')
        
        plt.subplot(2, 3, 6)
        sns.barplot(x='Warehouse', y='Backorder_Rate', data=filtered_df, palette='Reds')
        plt.title('Backorder Rate')
        plt.ylabel('Percentage (%)')
        
        plt.tight_layout()
        plt.show()
    
    display(warehouse_filter)
    widgets.interactive(update_dashboard, warehouse=warehouse_filter)
    
# Run the dashboard function
generate_inventory_dashboard()
