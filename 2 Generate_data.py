import pandas as pd
import numpy as np
from datetime import datetime
import random

np.random.seed(42)
random.seed(42)

# Define all regions
countries_regions = {
    'Kenya': ['Nairobi', 'Coast', 'Rift Valley'],
    'Nigeria': ['Lagos', 'Kano', 'Rivers'],
    'Uganda': ['Central', 'Western', 'Eastern'],
    'Ghana': ['Greater Accra', 'Ashanti', 'Northern'],
    'Ethiopia': ['Addis Ababa', 'Oromia', 'Amhara'],
    'Rwanda': ['Kigali', 'Northern', 'Southern'],
    'Malawi': ['Lilongwe', 'Blantyre', 'Mzuzu'],
    'Tanzania': ['Dar es Salaam', 'Mbeya', 'Mwanza']
}

# Flatten into a list of region identifiers (e.g., "Kenya: Nairobi")
all_regions = []
for country, region_list in countries_regions.items():
    for region in region_list:
        all_regions.append(f"{country}: {region}")

print(f"Total time series: {len(all_regions)}")  # Should be 24

# Base demand (visits per day) – vary by country/region size
# We'll assign a base value per region using a simple rule
base_demand_map = {}
for country, region_list in countries_regions.items():
    # Base country average: Kenya 120, Nigeria 150, Uganda 100, Ghana 110, Ethiopia 90, Rwanda 80, Malawi 70, Tanzania 105
    country_base = {
        'Kenya': 120, 'Nigeria': 150, 'Uganda': 100, 'Ghana': 110,
        'Ethiopia': 90, 'Rwanda': 80, 'Malawi': 70, 'Tanzania': 105
    }[country]
    for region in region_list:
        # Add small variation per region (±10% random)
        region_mult = random.uniform(0.9, 1.1)
        base_demand_map[f"{country}: {region}"] = int(country_base * region_mult)


# Time range
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Seasonality function (same as before)
def seasonal_factor(date):
    dow = date.weekday()
    weekend = 1.2 if dow == 5 else (1.1 if dow == 6 else 1.0)
    month_day = date.day
    mid_month = 1.0 + 0.15 * np.exp(-((month_day - 15)**2) / 100)
    return weekend * mid_month


# Generate rows
rows = []
for date in date_range:
    for region_id in all_regions:
        base = base_demand_map[region_id]
        seasonal = seasonal_factor(date)
        noise = np.random.normal(1.0, 0.1)
        demand = int(base * seasonal * noise)
        demand = max(0, demand)
        
        # Add artificial spike for Uganda: Western in October 2025 (test period)
        if region_id == "Uganda: Western" and date.year == 2025 and date.month == 10:
            spike_multiplier = 4.0   # 4x normal demand
            demand = int(demand * spike_multiplier)
        
        rows.append({
            'date': date.strftime('%Y-%m-%d'),
            'country': region_id.split(': ')[0],
            'region': region_id.split(': ')[1],
            'region_id': region_id,
            'client_visits': demand
        })

df = pd.DataFrame(rows)
print(f"✅ Generated {len(df)} rows.")
print(df.head())
print("\nSummary by region (first 5):")
print(df.groupby('region_id')['client_visits'].describe().head())

# Save
df.to_csv('2 msi_health_data.csv', index=False)
print("\n Saved as '3 msi_health_data.csv'")