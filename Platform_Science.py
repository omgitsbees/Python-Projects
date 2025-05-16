import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Number of data points to generate
num_rows = 2000

# Generate a list of vehicle IDs
vehicle_ids = [f"Vehicle_{i+1:03d}" for i in range(200)]
random_vehicle = [random.choice(vehicle_ids) for _ in range(num_rows)]

# Generate timestamps for the data
start_date = datetime(2025, 5, 1)
time_stamps = [start_date + timedelta(hours=i) for i in range(num_rows)]

# Generate driver IDs
driver_ids = [f"Driver_{i+1:03d}" for i in range(100)]
random_driver = [random.choice(driver_ids) for _ in range(num_rows)]

# Generate trip IDs
trip_ids = [f"Trip_{i+1:04d}" for i in range(500)]
random_trip = [random.choice(trip_ids) for _ in range(num_rows)]

# Generate location data (latitude and longitude)
def generate_location():
    # Approximate range around a central location (e.g., within a region)
    base_lat = 47.6062  # Approximate latitude of Seattle
    base_lon = -122.3321 # Approximate longitude of Seattle
    lat = np.random.normal(base_lat, 0.5)
    lon = np.random.normal(base_lon, 0.7)
    return round(lat, 4), round(lon, 4)

locations = [generate_location() for _ in range(num_rows)]
latitude = [loc[0] for loc in locations]
longitude = [loc[1] for loc in locations]

# Generate speed data (in mph)
speed = np.random.normal(loc=55, scale=20, size=num_rows).clip(0, 80).round(1)

# Generate fuel consumption data (in gallons per hour)
fuel_consumption = np.random.normal(loc=5, scale=1.5, size=num_rows).clip(1, 15).round(2)

# Generate engine load (%)
engine_load = np.random.randint(0, 101, size=num_rows)

# Generate diagnostic trouble codes (as strings, some might be NaN)
dtc_codes = [f"DTC_{random.randint(100, 999)}" if random.random() < 0.1 else None for _ in range(num_rows)]

# Generate harsh driving events (boolean)
harsh_braking = np.random.choice([True, False], size=num_rows, p=[0.05, 0.95])
harsh_acceleration = np.random.choice([True, False], size=num_rows, p=[0.03, 0.97])
harsh_cornering = np.random.choice([True, False], size=num_rows, p=[0.02, 0.98])

# Generate idling status (boolean)
is_idling = np.random.choice([True, False], size=num_rows, p=[0.08, 0.92])

# Create the DataFrame
data = pd.DataFrame({
    'timestamp': time_stamps,
    'vehicle_id': random_vehicle,
    'driver_id': random_driver,
    'trip_id': random_trip,
    'latitude': latitude,
    'longitude': longitude,
    'speed_mph': speed,
    'fuel_consumption_gph': fuel_consumption,
    'engine_load_percent': engine_load,
    'dtc_code': dtc_codes,
    'harsh_braking': harsh_braking,
    'harsh_acceleration': harsh_acceleration,
    'harsh_cornering': harsh_cornering,
    'is_idling': is_idling
})

# Save the DataFrame to a CSV file
data.to_csv('fleet_telematics_data.csv', index=False)

print("Dataset 'fleet_telematics_data.csv' generated successfully!")