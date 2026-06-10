import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

# Load the data 
df = pd.read_csv('8 Uganda_client_demand_forecast.csv', parse_dates=['date'])
df.set_index('date', inplace=True)

# Pick the region that has the spike (Central, because we added spike in October 2025)
region_to_forecast = "Central"
series = df[df['region'] == region_to_forecast]['client_visits'].copy()

# Train / test split: train = before Oct 2025, test = Oct-Dec 2025
train = series[series.index < '2025-10-01']
test = series[series.index >= '2025-10-01']

print(f"Training days: {len(train)}")
print(f"Test days: {len(test)}")
print(f"Spike expected in test period? {'Yes' if (test > 2*train.median()).any() else 'Check data'}")

# Fit Exponential Smoothing model
model = ExponentialSmoothing(
    train,
    trend='add',
    seasonal='add',
    seasonal_periods=7
).fit()

# Forecast
forecast = model.forecast(len(test))

# Anomaly detection bounds (using training residuals)
residuals = train - model.fittedvalues
residual_std = residuals.std()
upper_bound = forecast + 2 * residual_std
lower_bound = forecast - 2 * residual_std

# Identify anomalies in test period
anomalies = test[(test > upper_bound) | (test < lower_bound)]

# Evaluation
mae = mean_absolute_error(test, forecast)
mape = mean_absolute_percentage_error(test, forecast) * 100
print(f"\nTest MAE: {mae:.1f} visits")
print(f"Test MAPE: {mape:.1f}%")
print(f"Anomalies detected: {len(anomalies)} days")
if len(anomalies) > 0:
    print("Anomaly dates:", anomalies.index.strftime('%Y-%m-%d').tolist())

# Plot
plt.figure(figsize=(12, 5))
plt.plot(train.index, train, label='Training data', color='blue', alpha=0.6)
plt.plot(test.index, test, label='Actual (test)', color='green')
plt.plot(forecast.index, forecast, label='Forecast', color='red', linestyle='--')
plt.fill_between(forecast.index, lower_bound, upper_bound, color='gray', alpha=0.2, label='95% prediction band')
plt.scatter(anomalies.index, anomalies, color='red', s=80, label='Anomalies', zorder=5, edgecolors='black')
plt.title(f'Client Demand Forecast with Anomaly Detection – {region_to_forecast}')
plt.xlabel('Date')
plt.ylabel('Client Visits')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()