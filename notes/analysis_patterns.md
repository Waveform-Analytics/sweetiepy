# Analysis Patterns Documentation

This document outlines the key analysis patterns and approaches used in the Loopy Basic project for Type 1 diabetes data analysis.

## CGM-Focused Time-Series Analysis

The primary focus of this project is on Continuous Glucose Monitor (CGM) data analysis to identify patterns and trends for optimizing diabetes management.

### Time-Scale Analysis

- **Focus on manageable time periods**: Analyze weeks or months of data rather than viewing all 243K+ readings at once
- **Temporal patterns**: Identify patterns at specific times of day or days of the week
- **Trend identification**: Discover trends that can help optimize diabetes management

### Analysis Workflow

1. **Exploratory analysis**: Use marimo notebooks for interactive data exploration
2. **Pattern discovery**: Identify recurring patterns in glucose levels
3. **Statistical analysis**: Calculate metrics for specific time periods
4. **Treatment correlation**: ✅ **IMPLEMENTED** Correlate CGM data with treatment settings using MergedDataAccess

## Key Analysis Approaches

### Time-of-Day Patterns

- Hourly glucose trends
- Meal-time response patterns
- Overnight glucose stability

### Day-of-Week Patterns

- Weekday vs. weekend differences
- Activity-related patterns

### Statistical Summaries

- Average glucose by time period
- Time in range metrics
- Variability measures
- Hypoglycemia and hyperglycemia frequency

## Data Processing Pipeline

1. **Data retrieval**: Query specific time ranges from MongoDB
2. **Data cleaning**: Handle missing values and outliers
3. **Conversion to pandas**: Transform MongoDB documents to pandas DataFrames with PyArrow backend
4. **Time-series preparation**: Process timestamps and prepare for time-series analysis
5. **Visualization**: Generate plots and charts for pattern identification
6. **Statistical analysis**: Calculate metrics and identify significant patterns

## Visualization Approaches

- Time-series plots for trend visualization
- Heatmaps for time-of-day patterns
- Box plots for variability analysis
- Histograms for distribution analysis

## CGM + Pump Settings Correlation Analysis (v0.2.0)

### Time-Synchronized Analysis

The MergedDataAccess module enables powerful correlation analysis by synchronizing CGM readings with active pump settings:

```python
from sweetiepy.data.merged import MergedDataAccess

with MergedDataAccess() as merged:
    # Get CGM data with active pump settings at each timestamp
    df = merged.get_merged_cgm_and_settings(days=7)
    
    # Each row contains:
    # - dateTime: CGM reading timestamp
    # - sgv: Glucose value (mg/dL)  
    # - active_basal: Basal rate active at this time (u/h)
    # - active_carb_ratio: Carb ratio active at this time (g/u)
    # - active_isf: Insulin sensitivity factor active at this time (mg/dL per unit)
    # - hour_of_day, day_of_week: Time-based features
```

### Key Analysis Patterns

#### Settings Effectiveness Analysis
- **Basal rate impact**: Compare glucose outcomes across different basal rates
- **Carb ratio effectiveness**: Analyze post-meal glucose control by carb ratio
- **ISF appropriateness**: Evaluate correction effectiveness by insulin sensitivity factor

#### Temporal Settings Analysis
- **Time-of-day patterns**: How the same settings perform at different hours
- **Day-of-week variations**: Weekend vs weekday effectiveness
- **Seasonal patterns**: Long-term settings performance trends

#### Treatment Context Analysis
```python
# Include recent treatment context
df_with_treatments = merged.get_merged_with_recent_treatments(
    days=3, 
    lookback_hours=4
)

# Now includes:
# - insulin_last_4h: Total insulin in prior 4 hours
# - carbs_last_4h: Total carbs in prior 4 hours
```

### Correlation Analysis Methods

#### Statistical Correlations
```python
analysis = merged.analyze_settings_correlation(df)

# Returns correlations like:
# - active_basal vs glucose: -0.203 (negative = lower basal → higher glucose)
# - active_carb_ratio vs glucose: +0.235 (positive = higher ratio → higher glucose)
# - active_isf vs glucose: +0.194 (positive = higher ISF → higher glucose)
```

#### Grouped Analysis
```python
# Average glucose by basal rate
basal_analysis = df.groupby('active_basal')['sgv'].agg([
    'mean', 'std', 'count'
])

# Time patterns with settings
hourly_patterns = df.groupby(['hour_of_day', 'active_basal'])['sgv'].mean()
```

### Visualization Patterns

- **Scatter plots**: Glucose over time colored by basal rate
- **Box plots**: Glucose distribution by settings values
- **Heatmaps**: Settings effectiveness by time of day
- **Line plots**: Daily basal rate schedule overlaid with glucose patterns

### Analysis Insights

This merged analysis enables discovery of:
- **Optimal settings timing**: When different basal rates work best
- **Settings adjustments**: Data-driven recommendations for pump programming
- **Pattern recognition**: Recurring glucose patterns tied to specific settings
- **Treatment effectiveness**: How well current settings achieve target ranges

## Future Analysis Goals

- **Machine learning models**: Predict optimal settings based on historical outcomes
- **Meal response pattern identification**: Enhanced with carb ratio effectiveness
- **Exercise impact analysis**: Correlate with temporary basal adjustments
- **Sleep quality correlation**: Night-time basal effectiveness analysis
- **Automated settings recommendations**: AI-driven pump programming suggestions