import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Create weekly data for 2024 and first half of 2025
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 6, 30)
weeks = pd.date_range(start=start_date, end=end_date, freq='W-WED')

# Regions
treatment_region = "Western"
control_region = "Eastern"
country = "Uganda"

# Parallel trends: both regions start similar
# Treatment gets a lift after Jan 1, 2025
data = []
for week in weeks:
    is_post = week >= datetime(2025, 1, 1)
    
    for region in [treatment_region, control_region]:
        # Base demand (visits per week)
        base = 200 if region == treatment_region else 180
        
        # Seasonal pattern (slight)
        seasonal = 1 + 0.1 * np.sin(2 * np.pi * week.timetuple().tm_yday / 365)
        
        # Random noise
        noise = np.random.normal(1.0, 0.08)
        
        # Treatment effect: +40% in post period for treatment region only
        treatment_effect = 1.4 if (region == treatment_region and is_post) else 1.0
        
        visits = int(base * seasonal * noise * treatment_effect)
        visits = max(0, visits)
        
        data.append({
            'date': week.strftime('%Y-%m-%d'),
            'country': country,
            'region': region,
            'is_post': 1 if is_post else 0,
            'is_treatment': 1 if region == treatment_region else 0,
            'client_visits': visits
        })

df = pd.DataFrame(data)
print(f"Generated {len(df)} rows")
print(df.head(10))
print("\nGroup means:")
print(df.groupby(['is_post', 'region'])['client_visits'].mean())

df.to_csv('11 Uganda_campaign.csv', index=False)
print("\nSaved as '11_Uganda_campaign.csv'")