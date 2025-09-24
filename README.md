# Server Performance Analysis

This project provides comprehensive analysis tools for server performance data including CPU, Memory, Network, and Temperature metrics.

## Features

### 1. Descriptive Statistics
- Calculate mean, median, standard deviation, min, max, quartiles for all metrics
- Provides overview of average performance and variability

### 2. Distribution Analysis
- Statistical tests to check if data follows normal distribution
- Kolmogorov-Smirnov test for normality
- Skewness and kurtosis analysis
- Essential for choosing appropriate statistical methods

### 3. Time Pattern Analysis
- Hourly performance patterns to identify peak usage times
- Daily patterns (when multiple days available)
- Helps optimize workload scheduling

### 4. Data-Driven Alert Thresholds
- Automatic calculation of warning and critical thresholds
- Multiple methods: percentile-based, standard deviation, IQR
- Anomaly detection based on calculated thresholds

### 5. Optimization Recommendations
- Concrete, actionable recommendations based on analysis results
- CPU optimization strategies
- Memory management suggestions
- Network optimization advice
- Temperature monitoring alerts

### 6. Visualizations
- Time series plots for all metrics
- Distribution histograms
- Correlation heatmap
- All plots saved as high-resolution PNG files

## Usage

### Basic Analysis
```bash
python app/CPU_Analysis/data_analysis.py --csv data/server_usage_data.csv
```

### Using Individual Functions
```python
from app.CPU_Analysis.data_analysis import *
from app.CPU_Analysis.graphs import generate_all_visualizations

# Load data
df = load_csv("data/server_usage_data.csv")

# Get descriptive statistics
stats = calculate_descriptive_statistics(df)
print_descriptive_statistics(stats)

# Analyze distributions
dist_analysis = analyze_data_distribution(df)
print_distribution_analysis(dist_analysis)

# Calculate thresholds and detect anomalies
thresholds = calculate_alertness_thresholds(df, method='percentile')
anomalies = detect_anomalies(df, thresholds)

# Generate recommendations
recommendations = generate_optimization_recommendations(stats, anomalies, {})
for rec in recommendations:
    print(rec)

# Generate all visualizations
time_patterns = analyze_time_patterns(df)
generate_all_visualizations(df, time_patterns, thresholds, anomalies, "data/plot")
```

## Key Findings from Analysis

Based on Emma's analysis approach, this tool identified several critical insights:

1. **CPU Usage Patterns**: Peak usage during hours 7-8 (morning) and hour 1 (night maintenance)
2. **Memory Management**: High variability suggests need for memory optimization
3. **Network Saturation**: Reaching maximum capacity, requiring bandwidth optimization
4. **Temperature Concerns**: Peak temperatures require cooling system attention

## Emma's Methodology

This implementation follows Emma's analytical approach:

1. **Data Overview**: Start with descriptive statistics to understand overall performance
2. **Distribution Validation**: Check data distribution for appropriate statistical methods
3. **Pattern Recognition**: Identify time-based patterns for workload optimization
4. **Threshold-Based Monitoring**: Implement data-driven alerting systems
5. **Actionable Insights**: Generate concrete recommendations for optimization

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computations
- scipy: Statistical tests and analysis
- matplotlib: Basic plotting
- seaborn: Advanced statistical visualizations

## Output Files

All visualization plots are automatically saved to the `data/plot/` directory:

- `performance_timeseries.png`: Time series plots of all metrics
- `performance_distributions.png`: Distribution histograms  
- `correlation_heatmap.png`: Correlation matrix visualization
- `hourly_patterns.png`: Hourly performance patterns
- `anomaly_detection.png`: Performance metrics with threshold lines and anomaly highlights

## Project Structure

```
CPU_Analysis/
├── app/
│   └── CPU_Analysis/
│       ├── data_analysis.py    # Main analysis functions
│       └── graphs.py          # Visualization functions
├── data/
│   ├── server_usage_data.csv  # Input data
│   └── plot/                  # Generated visualization files
│       ├── performance_timeseries.png
│       ├── performance_distributions.png
│       ├── correlation_heatmap.png
│       ├── hourly_patterns.png
│       └── anomaly_detection.png
├── README.md
└── requirements files...
```
