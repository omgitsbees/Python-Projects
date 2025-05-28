import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Configuration
num_records = 75000  # Number of records to generate
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31) # Approx 2 years of data

# Possible values
event_types = [
    'usdc_payment_processed', 'usdc_transfer_out', 'usdc_transfer_in',
    'usdc_mint', 'usdc_burn', 'api_call_payments', 'api_call_accounts',
    'product_signup_business', 'product_feature_used', 'circle_account_deposit',
    'circle_account_withdrawal', 'cross_chain_transfer_initiated', 'cross_chain_transfer_completed'
]
products = [
    'Circle Payments API', 'Circle Accounts API', 'USDC Platform Services',
    'Web3 Services', 'Circle Mint', 'Cross-Chain Transfer Service', 'Yield Product A', 'None' # None for general USDC movements
]
blockchains = ['Ethereum', 'Solana', 'Avalanche', 'TRON', 'Polygon', 'Stellar', 'Algorand'] # Common for USDC
regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'MEA']
business_types = ['E-commerce', 'FinTech', 'Crypto Exchange', 'Gaming', 'SaaS', 'Creator Economy', 'Institutional Investor', 'Individual Developer']
acquisition_channels = ['Organic', 'Paid Search', 'Referral Program', 'Direct Sales', 'Partnership', 'Content Marketing']
transaction_statuses = ['Completed', 'Pending', 'Failed', 'Reversed']

data = []
current_usdc_circulation = 40_000_000_000  # Starting circulation (e.g., early 2023)
usdc_growth_factor_daily = (60/40)**(1/(365*1.5)) # Rough daily growth to reach 60B from 40B in 1.5 years

# Generate User IDs (businesses or significant individual users)
num_users = int(num_records / 50) # Average 50 events per user
user_ids = [f"USER_{1000+i}" for i in range(num_users)]
user_data = {}
for user_id in user_ids:
    user_data[user_id] = {
        'join_date': start_date + timedelta(days=random.randint(0, (end_date - start_date).days // 2)),
        'business_type': random.choice(business_types),
        'region': random.choice(regions),
        'acquisition_channel': random.choice(acquisition_channels)
    }


for i in range(num_records):
    event_timestamp = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    user_id = random.choice(user_ids)

    # Ensure event is after user join date
    if event_timestamp < user_data[user_id]['join_date']:
        event_timestamp = user_data[user_id]['join_date'] + timedelta(days=random.randint(1, 90))
        if event_timestamp > end_date: # cap at end_date
            event_timestamp = end_date - timedelta(days=random.randint(1,5))


    event_type = random.choices(
        event_types,
        weights=[0.2, 0.15, 0.15, 0.05, 0.03, 0.1, 0.1, 0.05, 0.07, 0.03, 0.03, 0.02, 0.02], # Biased towards common events
        k=1
    )[0]

    product_name = 'None'
    transaction_id = None
    amount_usdc = None
    currency = 'USDC'
    blockchain = 'None'
    status = 'Completed'

    if 'api_call' in event_type:
        product_name = event_type.split('_')[-1].capitalize() + " API"
        if 'Payments' in product_name : product_name = 'Circle Payments API'
        if 'Accounts' in product_name : product_name = 'Circle Accounts API'
        amount_usdc = None # API calls might not have direct USDC amount
    elif 'product_signup' in event_type:
        product_name = random.choice([p for p in products if p not in ['None', 'Circle Mint']])
        acquisition_channel_for_event = user_data[user_id]['acquisition_channel']
    elif 'product_feature_used' in event_type:
        product_name = random.choice([p for p in products if p != 'None'])
    elif 'usdc_' in event_type or 'circle_account' in event_type or 'cross_chain' in event_type:
        transaction_id = f"TXN_{random.randint(100000000, 999999999)}"
        blockchain = random.choice(blockchains)
        status = random.choices(transaction_statuses, weights=[0.90, 0.05, 0.04, 0.01], k=1)[0]

        if event_type == 'usdc_mint':
            amount_usdc = random.uniform(50000, 5000000) # Larger amounts for minting
            current_usdc_circulation += amount_usdc
            product_name = 'Circle Mint'
        elif event_type == 'usdc_burn':
            amount_usdc = random.uniform(10000, 2000000)
            current_usdc_circulation -= amount_usdc
            product_name = 'Circle Mint'
        elif 'transfer' in event_type or 'payment' in event_type or 'deposit' in event_type or 'withdrawal' in event_type:
            if user_data[user_id]['business_type'] in ['Institutional Investor', 'Crypto Exchange']:
                amount_usdc = random.uniform(10000, 10000000)
            elif user_data[user_id]['business_type'] == 'E-commerce':
                 amount_usdc = random.uniform(50, 5000) # Smaller B2C or B2B payments
            else:
                amount_usdc = random.uniform(100, 100000)
        if status == 'Failed' or status == 'Reversed':
            pass # Amount still logged but transaction didn't effectively go through as intended
    else: # Other event types
        product_name = random.choice(products)


    # Simulate growth in USDC circulation reflected in overall activity (very simplified)
    # This is a conceptual scaling, not a precise reflection of total circulation in each transaction.
    # A better approach for circulation would be a separate timeseries, but this biases amounts upwards over time.
    days_from_start = (event_timestamp - start_date).days
    dynamic_scaling_factor = usdc_growth_factor_daily ** days_from_start
    if amount_usdc:
        amount_usdc *= (0.5 + random.random()) # Add some randomness to scaling
        amount_usdc = round(amount_usdc * dynamic_scaling_factor, 2)


    data.append({
        'EventID': f"EVT_{10000+i}",
        'Timestamp': event_timestamp,
        'UserID': user_id,
        'UserJoinDate': user_data[user_id]['join_date'],
        'UserBusinessType': user_data[user_id]['business_type'],
        'UserRegion': user_data[user_id]['region'],
        'UserAcquisitionChannel': user_data[user_id]['acquisition_channel'] if event_type == 'product_signup_business' else None,
        'EventType': event_type,
        'ProductName': product_name,
        'Blockchain': blockchain if blockchain != 'None' else (random.choice(blockchains) if 'usdc_' in event_type else None),
        'TransactionID': transaction_id,
        'AmountUSDC': amount_usdc if amount_usdc else 0.0, # Ensure numeric for aggregation
        'Currency': currency if amount_usdc else None,
        'TransactionStatus': status if transaction_id else None,
        'CurrentEstimatedUSDCSupply': round(current_usdc_circulation * dynamic_scaling_factor,0) if 'mint' in event_type or 'burn' in event_type else None # Only log this for mint/burn events to show supply changes
    })

df = pd.DataFrame(data)

# Sort by timestamp
df = df.sort_values(by='Timestamp').reset_index(drop=True)

# Refine CurrentEstimatedUSDCSupply to be a forward fill or based on actual mint/burn sum
# For simplicity, let's calculate a running total of mints - burns for a 'NetIssuance'
df['NetAmount'] = df.apply(lambda row: row['AmountUSDC'] if row['EventType'] == 'usdc_mint' and row['TransactionStatus'] == 'Completed'
                           else (-row['AmountUSDC'] if row['EventType'] == 'usdc_burn' and row['TransactionStatus'] == 'Completed' else 0), axis=1)
initial_circulation_at_data_start = 40_000_000_000 # The actual circulation at the *start of the dataset's timeframe*
df['RunningUSDCSupply'] = df['NetAmount'].cumsum() + initial_circulation_at_data_start
df.drop(columns=['CurrentEstimatedUSDCSupply', 'NetAmount'], inplace=True)


print("Sample of the generated dataset:")
print(df.head())
print(f"\nGenerated {len(df)} records.")
print(f"\nDate range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
print(f"\nEstimated USDC supply at end of period: {df['RunningUSDCSupply'].iloc[-1]:,}")

# Potential KPIs you can derive for dashboards:
# - Daily/Weekly/Monthly Active Users (DAU/WAU/MAU)
# - Transaction Volume (sum of AmountUSDC) over time, by product, by region, by blockchain
# - Transaction Count over time, by product, by region, by blockchain
# - Average Transaction Value (ATV)
# - USDC Mint vs. Burn volume over time
# - Growth in RunningUSDCSupply
# - Product Adoption Rate (e.g., count of UserID per ProductName)
# - User Growth (new UserID by UserJoinDate)
# - API Call frequency
# - Failed Transaction Rate (count where TransactionStatus is 'Failed' / total transactions)

# Save to CSV
try:
    df.to_csv('circle_business_operations_data.csv', index=False)
    print("\nDataset saved to circle_business_operations_data.csv")
except Exception as e:
    print(f"\nError saving CSV: {e}")