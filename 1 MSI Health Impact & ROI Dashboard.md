MSI Health Impact & ROI Dashboard

Author: David Lyatuu  
Date:   10 June 2026  
GitHub: https://github.com/david-isights  
Tableau Public: (https://public.tableau.com/app/profile/david.lyatuu/viz/6MSI_health_dashboard/Dashboard1?publish=yes)

Overview
Portfolio demonstrating data engineering, analytics, causal inference, and visualization – aligned with the Regional Data Analyst role at MSI Reproductive Choices.

Projects

1. MSI Health Impact Dashboard (Tableau)
- Goal: Visualize program reach, ROI, and service performance across 8 African countries.
- Data pipeline: Python generates 9,000+ rows of realistic daily service data (client visits, costs, social value).
- Key visuals: ROI map (region-level), time-series by service, KPI cards, drill-down filters.
- Result: Interactive dashboard showing regional ROI disparities and service volume trends.

2. Client Demand Forecasting & Anomaly Detection (Python)
- Goal: Predict daily client demand and detect spikes.
- Method: Exponential Smoothing (ETS) with weekly seasonality; anomaly detection via prediction intervals.
- Result: Forecast MAPE ~9% (normal period); successfully flagged a 3.5x spike in Uganda: Western.
- Files: `7_Region_forecast_data.py`, `9_Uganda_anomalies.py`

3. Causal Impact Evaluation  Difference-in-Differences (Python)
- Goal: Measure the causal effect of a hypothetical MSI campaign in Western Uganda.
- Method: DiD regression comparing treatment (Western) vs control (Eastern) before/after campaign start.
- Result: Campaign led to +82.9 additional weekly visits (p < 0.001) - statistically significant.
- Files: `10_Uganda_DiD.py`, `12_Uganda_DiD_analyze.py`

4. Power BI Dashboard (Complementary)
- Goal: Show same data using Power BI's decomposition tree and small multiples.
- Key visual: Decomposition tree automatically identifies drivers of client volume (country → region → facility type → service type).
- Access: `.pbix` file included in repo; screenshots and video walkthrough in `assets/` folder.

Mission Alignment
I unequivocally support reproductive choice and am committed to using data to improve access to family planning and maternal health services – especially in underserved regions.

How to Reproduce
1. Clone this repo.
2. Install dependencies: `pip install pandas numpy statsmodels matplotlib seaborn scikit-learn`
3. Run the Python scripts in order (they generate CSVs in the same folder).
4. Open Tableau/Power BI files and connect to the CSVs.

Automated Reporting Pipeline (Concept)
In a production environment, I would:
- Schedule daily execution of the Python script using Windows Task Scheduler / cron.
- Configure Tableau Bridge or Power BI Gateway to refresh the dashboard automatically.
- Set up logging and error alerts.