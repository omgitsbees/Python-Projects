import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import ipaddress

# Set random seed for reproducibility
np.random.seed(42)
fake = Faker()

def generate_fraud_dataset(num_records=10000, fraud_percentage=0.1):
    """Generate a dataset with fraud patterns."""
    
    # Calculate number of fraud records
    num_fraud = int(num_records * fraud_percentage)
    
    data = {
        'SellerID': [],
        'Email': [],
        'AccountCreationDate': [],
        'PhysicalLocation': [],
        'IPAddress': [],
        'CreditCardNumber': [],
        'NumSales': [],
        'InventoryCount': [],
        # Additional columns
        'LastLoginDate': [],
        'AccountStatus': [],
        'VerificationLevel': [],
        'ReturnRate': [],
        'AverageTransactionValue': [],
        'CustomerRating': [],
        'FailedLoginAttempts': [],
        'PaymentMethodsCount': [],
        'ShippingSpeedAvg': [],
        'ListingUpdateFrequency': [],
        'DisputeCount': [],
        'IsFraud': []
    }

    # Generate legitimate records
    for _ in range(num_records - num_fraud):
        data = add_legitimate_record(data)

    # Generate fraud patterns
    fraud_patterns = [
        generate_shared_credentials() for _ in range(int(num_fraud/3))
    ]
    
    # Add fraud records
    for _ in range(num_fraud):
        if random.random() < 0.3 and fraud_patterns:  # 30% chance to use shared credentials
            pattern = random.choice(fraud_patterns)
            data = add_fraud_record(data, shared_credentials=pattern)
        else:
            data = add_fraud_record(data)

    df = pd.DataFrame(data)
    return df

def generate_shared_credentials():
    """Generate shared credentials for fraud patterns."""
    return {
        'email': fake.email(),
        'ip': fake.ipv4(),
        'credit_card': fake.credit_card_number()
    }

def add_legitimate_record(data):
    """Add a legitimate record to the dataset."""
    creation_date = fake.date_time_between(start_date='-2y', end_date='now')
    
    data['SellerID'].append(fake.uuid4())
    data['Email'].append(fake.email())
    data['AccountCreationDate'].append(creation_date)
    data['PhysicalLocation'].append(fake.city())
    data['IPAddress'].append(fake.ipv4())
    data['CreditCardNumber'].append(fake.credit_card_number())
    data['NumSales'].append(random.randint(0, 1000))
    data['InventoryCount'].append(random.randint(0, 500))
    
    # Additional columns
    data['LastLoginDate'].append(fake.date_time_between(start_date=creation_date))
    data['AccountStatus'].append(random.choice(['Active', 'Active', 'Active', 'Suspended', 'Pending']))
    data['VerificationLevel'].append(random.choice([1, 2, 3]))
    data['ReturnRate'].append(round(random.uniform(0, 0.15), 3))
    data['AverageTransactionValue'].append(round(random.uniform(10, 500), 2))
    data['CustomerRating'].append(round(random.uniform(4, 5), 1))
    data['FailedLoginAttempts'].append(random.randint(0, 3))
    data['PaymentMethodsCount'].append(random.randint(1, 4))
    data['ShippingSpeedAvg'].append(round(random.uniform(1, 5), 1))
    data['ListingUpdateFrequency'].append(random.randint(1, 30))
    data['DisputeCount'].append(random.randint(0, 2))
    data['IsFraud'].append(0)
    
    return data

def add_fraud_record(data, shared_credentials=None):
    """Add a fraudulent record to the dataset."""
    creation_date = fake.date_time_between(start_date='-6m', end_date='now')
    
    data['SellerID'].append(fake.uuid4())
    data['Email'].append(shared_credentials['email'] if shared_credentials else fake.email())
    data['AccountCreationDate'].append(creation_date)
    data['PhysicalLocation'].append(fake.city())
    data['IPAddress'].append(shared_credentials['ip'] if shared_credentials else fake.ipv4())
    data['CreditCardNumber'].append(shared_credentials['credit_card'] if shared_credentials else fake.credit_card_number())
    data['NumSales'].append(random.randint(50, 5000))  # Higher sales volume
    data['InventoryCount'].append(random.randint(0, 100))
    
    # Additional columns with fraud patterns
    data['LastLoginDate'].append(fake.date_time_between(start_date=creation_date))
    data['AccountStatus'].append(random.choice(['Active', 'Active', 'Flagged', 'Under Review']))
    data['VerificationLevel'].append(random.choice([1, 1, 1, 2]))  # Lower verification levels
    data['ReturnRate'].append(round(random.uniform(0.2, 0.4), 3))  # Higher return rates
    data['AverageTransactionValue'].append(round(random.uniform(400, 2000), 2))  # Higher transaction values
    data['CustomerRating'].append(round(random.uniform(2, 3.5), 1))  # Lower ratings
    data['FailedLoginAttempts'].append(random.randint(3, 10))  # More failed attempts
    data['PaymentMethodsCount'].append(random.randint(1, 2))  # Fewer payment methods
    data['ShippingSpeedAvg'].append(round(random.uniform(3, 7), 1))  # Slower shipping
    data['ListingUpdateFrequency'].append(random.randint(20, 50))  # More frequent updates
    data['DisputeCount'].append(random.randint(3, 10))  # More disputes
    data['IsFraud'].append(1)
    
    return data

if __name__ == "__main__":
    # Generate dataset
    df = generate_fraud_dataset(num_records=10000, fraud_percentage=0.1)
    
    # Save to CSV
    df.to_csv('fraud_analysis_dataset.csv', index=False)
    print(f"Generated dataset with {len(df)} records")
    print(f"Fraud records: {df['IsFraud'].sum()}")
    print("\nSample of fraud patterns:")
    print(df[df['IsFraud'] == 1].head())