import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os # Added to potentially help with path construction if needed, though not strictly necessary here

# --- Configuration for Data Generation ---
num_records = 2000  # Number of subscription events/transactions to generate
start_date = datetime(2023, 1, 1)
# Use current date from context: Friday, May 2, 2025 at 8:30:23 PM PDT
# To ensure reproducibility let's fix it to the date part for the script
end_date = datetime(2025, 5, 2)

# Sample data pools
partners = {
    1001: {"name": "Innovate Solutions Inc.", "segment": "SMB", "region": "Americas West"},
    1002: {"name": "CloudForward Tech", "segment": "Mid-Market", "region": "Americas East"},
    1003: {"name": "Secure Networks LLC", "segment": "SMB", "region": "Americas Central"},
    1004: {"name": "Enterprise IT Masters", "segment": "Enterprise", "region": "Americas West"},
    1005: {"name": "NextGen MSP", "segment": "Mid-Market", "region": "Americas East"},
    1006: {"name": "Apex Cloud Partners", "segment": "SMB", "region": "Americas Central"},
    1007: {"name": "Summit Technology Group", "segment": "Enterprise", "region": "Americas West"},
    1008: {"name": "Pinnacle IT", "segment": "Mid-Market", "region": "Americas East"},
}
partner_ids = list(partners.keys())

products = {
    201: {"name": "Microsoft 365 Business Premium", "vendor": "Microsoft", "category": "Productivity"},
    202: {"name": "Acronis Cyber Protect Cloud", "vendor": "Acronis", "category": "Backup & Security"},
    203: {"name": "SentinelOne Control", "vendor": "SentinelOne", "category": "Security"},
    204: {"name": "Azure Plan", "vendor": "Microsoft", "category": "Infrastructure"},
    205: {"name": "Proofpoint Essentials Security", "vendor": "Proofpoint", "category": "Security"},
    206: {"name": "Dropbox Business Standard", "vendor": "Dropbox", "category": "Collaboration"},
    207: {"name": "Bitdefender GravityZone", "vendor": "Bitdefender", "category": "Security"},
}
product_ids = list(products.keys())

event_types = ["New Subscription", "Renewal", "Upgrade", "Downgrade", "Cancellation"]
billing_status = ["Billed - Paid", "Billed - Pending Payment", "Billed - Overdue", "Not Billed Yet"]
sales_reps = ["SR001", "SR002", "SR003", "SR004", "SR005"]

# --- Helper Functions ---
def random_date(start, end):
    """Generate a random datetime between start and end."""
    return start + timedelta(
        # Get a random amount of seconds between start and end
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# --- Generate Data ---
data = []
for i in range(num_records):
    event_id = 50000 + i
    partner_id = random.choice(partner_ids)
    partner_info = partners[partner_id]
    product_id = random.choice(product_ids)
    product_info = products[product_id]
    event_type = random.choices(event_types, weights=[0.4, 0.3, 0.1, 0.05, 0.15], k=1)[0]
    event_date = random_date(start_date, end_date)

    # Simulate some logic based on event type
    quantity = random.randint(1, 250) if product_info["category"] != "Infrastructure" else 1
    mrr = 0
    if event_type != "Cancellation":
         # Simulate MRR based on product and quantity, add some randomness
         base_mrr = random.uniform(5, 50) if product_info["category"] != "Infrastructure" else random.uniform(50, 5000)
         mrr = round(base_mrr * quantity * random.uniform(0.9, 1.1), 2)


    sub_start_date = event_date - timedelta(days=random.randint(0, 30)) if event_type == "New Subscription" else event_date - timedelta(days=random.randint(30, 365))
    sub_end_date = None
    if event_type == "Cancellation":
         sub_end_date = event_date + timedelta(days=random.randint(1, 30))
         quantity = 0 # Cancelled means 0 quantity going forward
         mrr = 0
    elif product_info["category"] != "Infrastructure": # Assume non-infra has defined terms
         sub_end_date = sub_start_date + timedelta(days=random.choice([30, 90, 365]))


    data.append({
        "EventID": event_id,
        "PartnerID": partner_id,
        "PartnerName": partner_info["name"],
        "PartnerSegment": partner_info["segment"],
        "PartnerRegion": partner_info["region"],
        "ProductID": product_id,
        "ProductName": product_info["name"],
        "VendorName": product_info["vendor"],
        "ProductCategory": product_info["category"],
        "EventType": event_type,
        "EventDate": event_date.date(), # Store as date object
        "EventTimestamp": event_date, # Store full timestamp
        "SubscriptionStartDate": sub_start_date.date(),
        "SubscriptionEndDate": sub_end_date.date() if sub_end_date else None,
        "Quantity": quantity,
        "MonthlyRecurringRevenue (MRR)": mrr,
        "BillingStatus": random.choice(billing_status) if event_type != "Cancellation" else "N/A",
        "SalesRepresentative": random.choice(sales_reps),
        "SupportTicketRelated": random.choices([True, False], weights=[0.1, 0.9], k=1)[0] # Small chance a support ticket was related
    })

# --- Create DataFrame ---
df = pd.DataFrame(data)

# Ensure correct data types
df['EventDate'] = pd.to_datetime(df['EventDate'])
df['EventTimestamp'] = pd.to_datetime(df['EventTimestamp'])
df['SubscriptionStartDate'] = pd.to_datetime(df['SubscriptionStartDate'])
df['SubscriptionEndDate'] = pd.to_datetime(df['SubscriptionEndDate'], errors='coerce') # Handle None -> NaT
df['PartnerID'] = df['PartnerID'].astype(str) # Treat IDs as strings usually safer
df['ProductID'] = df['ProductID'].astype(str)
df['Quantity'] = df['Quantity'].astype(int)
df['MonthlyRecurringRevenue (MRR)'] = df['MonthlyRecurringRevenue (MRR)'].astype(float)
df['SupportTicketRelated'] = df['SupportTicketRelated'].astype(bool)

# --- Display Sample Data and Info ---
print("--- Sample Cloud Subscription Dataset ---")
print(f"Generated {len(df)} records.")
print("\n--- First 5 Rows ---")
# Using markdown for potentially better display in some environments
try:
    print(df.head().to_markdown(index=False))
except ImportError:
     print(df.head()) # Fallback to default print


print("\n--- DataFrame Info ---")
df.info()

print("\n--- Example Aggregation (MRR by Vendor) ---")
# This is the type of analysis the BI Analyst would perform
mrr_by_vendor = df.groupby('VendorName')['MonthlyRecurringRevenue (MRR)'].sum().reset_index()
mrr_by_vendor = mrr_by_vendor.sort_values('MonthlyRecurringRevenue (MRR)', ascending=False)
# Using markdown for potentially better display in some environments
try:
    print(mrr_by_vendor.to_markdown(index=False))
except ImportError:
    print(mrr_by_vendor) # Fallback to default print


# --- Save DataFrame to CSV File ---
csv_filename = "sample_pax8_subscription_data.csv"
try:
    df.to_csv(csv_filename, index=False, encoding='utf-8') # index=False prevents writing the pandas index as a column
    print(f"\n--- Success ---")
    print(f"Dataset successfully saved to: {os.path.abspath(csv_filename)}") # Show absolute path
except Exception as e:
    print(f"\n--- Error ---")
    print(f"Could not save dataset to CSV: {e}")