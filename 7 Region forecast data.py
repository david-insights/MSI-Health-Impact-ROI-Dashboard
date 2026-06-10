import pandas as pd
import numpy as np
from datetime import datetime
import random

np.random.seed(42)
random.seed(42)

# Parameters
regions = ['Northern', 'Central', 'Southern']
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Base demand per day for each region
base_demand = {
    'Northern': 120,
    'Central': 200,
    'Southern': 80
}

# Seasonality function
def seasonal_factor(date):
    dow = date.weekday()
    weekend = 1.2 if dow == 5 else (1.1 if dow == 6 else 1.0)
    month_day = date.day
    mid_month = 1.0 + 0.15 * np.exp(-((month_day - 15)**2) / 100)
    return weekend * mid_month

# Generate rows
rows = []
for date in date_range:
    for region in regions:
        base = base_demand[region]
        seasonal = seasonal_factor(date)
        noise = np.random.normal(1.0, 0.1)
        demand = int(base * seasonal * noise)
        demand = max(0, demand)
        
        # Spike in Central region, October 2025
        if region == 'Central' and date.year == 2025 and date.month == 10:
            spike_multiplier = 3.5
            demand = int(demand * spike_multiplier)
        
        rows.append({
            'date': date.strftime('%Y-%m-%d'),
            'region': region,
            'client_visits': demand
        })
        
df = pd.DataFrame(rows)
print(f"✅ Generated {len(df)} rows.")
print(df.head())
print(df.groupby('region')['client_visits'].describe())

# Save to CSV
df.to_csv('8 Uganda_client_demand_forecast.csv', index=False)
print("Saved as '8 Uganda_client_demand_forecast.csv'")