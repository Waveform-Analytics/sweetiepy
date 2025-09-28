# CGM + Pump Settings Merged Data Analysis

This document provides comprehensive documentation for the merged data functionality introduced in v0.2.0, which synchronizes CGM readings with active pump settings for advanced diabetes management analysis.

## Overview

The `MergedDataAccess` module solves a critical challenge in diabetes data analysis: **understanding the relationship between pump settings and glucose outcomes**. Previously, you could analyze CGM data or pump settings separately, but couldn't easily correlate them. This module merges CGM readings with the pump settings that were active at each reading time.

## The Problem It Solves

### Before: Separate Data Streams
- CGM readings: `[180 mg/dL at 3:00 PM]`
- Pump settings: `[Basal: 0.45 u/h, Carb Ratio: 13 g/u, ISF: 133 mg/dL per unit]`
- **Question**: Which settings were active when that 180 mg/dL reading occurred?

### After: Time-Synchronized Analysis
- Merged data: `[180 mg/dL at 3:00 PM, Basal: 0.45 u/h, CR: 13 g/u, ISF: 133]`
- **Analysis**: Now you can analyze how different settings affect glucose outcomes!

## Key Features

### 1. Time-Synchronized Settings Lookup
```python
from sweetiepy.data.merged import MergedDataAccess

with MergedDataAccess() as merged:
    # Get active basal rate at any specific time
    basal_rate = merged.get_active_basal_at_time(datetime(2025, 1, 15, 14, 30))
    
    # Get active carb ratio
    carb_ratio = merged.get_active_carb_ratio_at_time(datetime(2025, 1, 15, 14, 30))
    
    # Get active insulin sensitivity factor
    isf = merged.get_active_isf_at_time(datetime(2025, 1, 15, 14, 30))
```

### 2. Merged DataFrame Creation
```python
# Get CGM data enriched with pump settings
df = merged.get_merged_cgm_and_settings(days=7)

print(df.columns)
# Output: ['dateTime', 'sgv', 'trend', 'active_basal', 'active_carb_ratio', 
#          'active_isf', 'hour_of_day', 'day_of_week', 'time_of_day_category']
```

### 3. Treatment Context Analysis
```python
# Include recent insulin/carb treatments for context
df_with_context = merged.get_merged_with_recent_treatments(
    days=3, 
    lookback_hours=4
)

# Additional columns:
# - insulin_last_4h: Total insulin in prior 4 hours
# - carbs_last_4h: Total carbs in prior 4 hours
```

## Analysis Capabilities

### Settings Effectiveness Analysis

**Question**: Do higher basal rates improve glucose control?
```python
# Group glucose readings by basal rate
basal_analysis = df.groupby('active_basal')['sgv'].agg([
    ('Average Glucose', 'mean'),
    ('Std Dev', 'std'), 
    ('Readings', 'count'),
    ('% Time', lambda x: len(x) / len(df) * 100)
])

print(basal_analysis)
```

**Example Output**:
```
              Average Glucose  Std Dev  Readings  % Time
active_basal                                            
0.35                    200.0     61.7       483    24.3
0.45                    171.7     57.3      1507    75.7
```

**Insight**: Higher basal rate (0.45 u/h) correlates with better glucose control (171.7 vs 200.0 mg/dL).

### Time-of-Day Patterns

**Question**: How do settings perform at different times?
```python
# Analyze hourly patterns with settings
hourly = df.groupby('hour_of_day').agg({
    'sgv': ['mean', 'std'],
    'active_basal': 'first',
    'active_carb_ratio': 'first',
    'active_isf': 'first'
})

print("Hourly glucose patterns with active settings:")
for hour in range(0, 24, 3):
    row = hourly.loc[hour]
    print(f"{hour:02d}:00 - Glucose: {row[('sgv', 'mean')]:.0f} mg/dL, "
          f"Basal: {row[('active_basal', 'first')]:.2f} u/h")
```

### Statistical Correlations

**Question**: Which settings have the strongest impact on glucose?
```python
analysis = merged.analyze_settings_correlation(df)

if 'correlations' in analysis:
    for setting, correlation in analysis['correlations'].items():
        direction = "positive" if correlation > 0 else "negative"
        strength = "strong" if abs(correlation) > 0.5 else "moderate" if abs(correlation) > 0.3 else "weak"
        print(f"{setting}: {correlation:+.3f} ({strength} {direction})")
```

**Example Output**:
```
active_basal: -0.203 (weak negative)        # Lower basal → higher glucose
active_carb_ratio: +0.235 (weak positive)   # Higher CR → higher glucose  
active_isf: +0.194 (weak positive)          # Higher ISF → higher glucose
```

## Visualization Examples

### 1. Glucose Over Time by Basal Rate
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))
scatter = ax.scatter(df['dateTime'], df['sgv'], 
                    c=df['active_basal'], cmap='viridis', alpha=0.6)
ax.set_ylabel('Glucose (mg/dL)')
ax.axhline(y=70, color='red', linestyle='--', alpha=0.3)
ax.axhline(y=180, color='red', linestyle='--', alpha=0.3)
plt.colorbar(scatter, label='Basal Rate (u/h)')
plt.title('Glucose Readings Colored by Active Basal Rate')
```

### 2. Settings Schedule Visualization  
```python
# Plot daily basal rate schedule
hours = range(24)
basal_by_hour = [merged.get_active_basal_at_time(
    datetime.now().replace(hour=h, minute=0)) for h in hours]

plt.figure(figsize=(10, 4))
plt.step(hours, basal_by_hour, where='post', linewidth=2)
plt.xlabel('Hour of Day')
plt.ylabel('Basal Rate (u/h)')
plt.title('Daily Basal Rate Schedule')
plt.xticks(range(0, 24, 3))
plt.grid(True, alpha=0.3)
```

## Real-World Use Cases

### 1. Settings Optimization
**Scenario**: Your morning glucose is consistently high.
**Analysis**: 
```python
morning_data = df[df['hour_of_day'].between(6, 10)]
morning_analysis = morning_data.groupby('active_basal')['sgv'].mean()
print("Average morning glucose by basal rate:")
print(morning_analysis)
```
**Action**: If lower basal rates correlate with higher morning glucose, consider increasing morning basal.

### 2. Carb Ratio Effectiveness
**Scenario**: Post-meal spikes vary significantly.
**Analysis**:
```python
# Look at glucose 2-4 hours after carb entries (meal times)
post_meal = df_with_context[df_with_context['carbs_last_4h'] > 0]
cr_effectiveness = post_meal.groupby('active_carb_ratio')['sgv'].agg(['mean', 'count'])
print("Post-meal glucose by carb ratio:")
print(cr_effectiveness)
```
**Action**: Adjust carb ratios based on post-meal glucose outcomes.

### 3. Treatment Context Analysis
**Scenario**: Understanding glucose patterns with recent insulin.
**Analysis**:
```python
recent_insulin = df_with_context['insulin_last_3h'] > 0
with_insulin_avg = df_with_context[recent_insulin]['sgv'].mean()
without_insulin_avg = df_with_context[~recent_insulin]['sgv'].mean()

print(f"Average glucose WITH recent insulin: {with_insulin_avg:.1f} mg/dL")
print(f"Average glucose WITHOUT recent insulin: {without_insulin_avg:.1f} mg/dL")
```

## Technical Implementation

### Time-Based Settings Lookup
The module handles the complexity of time-based pump settings:
- **Basal rates**: Different rates for different hours (e.g., 0.4 u/h at 6 AM, 0.5 u/h at noon)
- **Carb ratios**: May vary by meal (e.g., 12 g/u for breakfast, 15 g/u for dinner)  
- **ISF**: Often changes throughout the day (e.g., 140 mg/dL/u morning, 120 mg/dL/u evening)

### Caching and Performance
- **Profile caching**: Pump settings are cached for 5 minutes to avoid repeated database queries
- **Efficient lookups**: Time-based binary search for active settings
- **PyArrow backend**: High-performance DataFrames for large datasets

### Error Handling
- **Missing profiles**: Graceful handling when pump profiles aren't available
- **Time parsing**: Robust parsing of different time formats (HH:MM:SS, seconds since midnight)
- **Data validation**: Ensures datetime columns are properly converted

## Best Practices

### 1. Choose Appropriate Time Periods
```python
# For settings analysis, 1-2 weeks is usually sufficient
df = merged.get_merged_cgm_and_settings(days=14)

# For pattern discovery, longer periods may be useful
df = merged.get_merged_cgm_and_settings(days=30)
```

### 2. Consider Treatment Context
```python
# Include treatment context for comprehensive analysis
df = merged.get_merged_with_recent_treatments(days=7, lookback_hours=4)
```

### 3. Filter and Clean Data
```python
# Remove extreme outliers
df_clean = df[(df['sgv'] >= 40) & (df['sgv'] <= 400)]

# Focus on specific time periods
weekend_data = df[df['day_of_week'].isin([5, 6])]  # Sat, Sun
weekday_data = df[df['day_of_week'].isin([0, 1, 2, 3, 4])]  # Mon-Fri
```

## Example Analysis Workflow

```python
from sweetiepy.data.merged import MergedDataAccess
import pandas as pd
import matplotlib.pyplot as plt

# 1. Get merged data
with MergedDataAccess() as merged:
    df = merged.get_merged_cgm_and_settings(days=14)
    
    # 2. Basic analysis
    analysis = merged.analyze_settings_correlation(df)
    print(f"Average glucose: {analysis['data_summary']['glucose_stats']['mean']:.1f} mg/dL")
    print(f"Time in range: {analysis['data_summary']['glucose_stats']['in_range_70_180']:.1f}%")
    
    # 3. Settings effectiveness
    if 'basal_rate_analysis' in analysis:
        print("\nGlucose by basal rate:")
        for rate, stats in analysis['basal_rate_analysis'].items():
            print(f"  {rate:.2f} u/h: {stats['mean']:.1f} mg/dL (n={stats['count']})")
    
    # 4. Time patterns
    hourly_patterns = df.groupby(['hour_of_day', 'active_basal'])['sgv'].mean()
    
    # 5. Visualization
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(df['dateTime'], df['sgv'], c=df['active_basal'], cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label='Basal Rate (u/h)')
    plt.axhline(y=70, color='red', linestyle='--', alpha=0.3)
    plt.axhline(y=180, color='red', linestyle='--', alpha=0.3)
    plt.title('CGM Readings with Active Basal Rates')
    plt.ylabel('Glucose (mg/dL)')
    plt.show()
```

## Future Enhancements

The merged data foundation enables future advanced analytics:

1. **Machine Learning Models**: Train models to predict optimal settings
2. **Automated Recommendations**: AI-driven suggestions for pump programming
3. **Comparative Analysis**: A/B test different settings approaches
4. **Integration**: Connect with other diabetes management platforms
5. **Real-time Analysis**: Live glucose and settings correlation monitoring

## Conclusion

The merged data functionality transforms diabetes data analysis from descriptive ("What happened?") to prescriptive ("What should I do?"). By understanding how pump settings affect glucose outcomes over time, you can make data-driven decisions to optimize diabetes management.

This capability represents a significant step toward personalized, evidence-based diabetes care using your own historical data.