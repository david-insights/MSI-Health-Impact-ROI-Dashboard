import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# Load data )
df_did = pd.read_csv('11 Uganda_campaign.csv', parse_dates=['date'])

# Parallel trends check (pre‑period)
pre_data = df_did[df_did['is_post'] == 0]
pre_pivot = pre_data.pivot(index='date', columns='region', values='client_visits')
pre_pivot['trend_diff'] = pre_pivot['Western'] - pre_pivot['Eastern']
print("Parallel trends check - pre-period difference:")
print(pre_pivot['trend_diff'].describe())
print(f"\nTrend difference is small and stable? Mean diff: {pre_pivot['trend_diff'].mean():.1f}")

# DiD regression
model = smf.ols('client_visits ~ is_post * is_treatment', data=df_did).fit()
print("\n" + "="*50)
print("DIFFERENCE-IN-DIFFERENCES RESULTS")
print("="*50)
print(model.summary().tables[1])

# The interaction coefficient = causal impact
coef = model.params['is_post:is_treatment']
p_value = model.pvalues['is_post:is_treatment']
print(f"\n Causal impact (treatment effect): {coef:.1f} additional visits per week")
print(f"P-value: {p_value:.4f} {'(SIGNIFICANT)' if p_value < 0.05 else '(not significant)'}")

# Plot
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_did, x='date', y='client_visits', hue='region', marker='o', ci=None)
plt.axvline(pd.Timestamp('2025-01-01'), color='red', linestyle='--', label='Campaign start')
plt.title('DiD: Client Visits Before/After Campaign (Uganda)')
plt.xlabel('Date')
plt.ylabel('Weekly Client Visits')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()