from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
import sys
import os

# Add the current directory to the path to import graphs module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from graphs import generate_all_visualizations

def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a server usage CSV file into a pandas DataFrame."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    
    df = pd.read_csv(p)
    
    # Convert time column to datetime
    if 'Time' in df.columns:
        df['Time'] = pd.to_datetime(df['Time'])
    elif 'dteday' in df.columns:
        df['dteday'] = pd.to_datetime(df['dteday'])
    
    return df


def calculate_descriptive_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate descriptive statistics for each metric (CPU, Memory, Network, Temperature).
    
    Args:
        df: DataFrame containing server usage data
        
    Returns:
        Dictionary containing statistics for each metric
    """
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    stats_dict = {}
    
    for metric in metrics:
        if metric in df.columns:
            stats_dict[metric] = {
                'mean': df[metric].mean(),
                'median': df[metric].median(),
                'std': df[metric].std(),
                'min': df[metric].min(),
                'max': df[metric].max(),
                'q1': df[metric].quantile(0.25),
                'q3': df[metric].quantile(0.75),
                'count': df[metric].count()
            }
    
    return stats_dict


def print_descriptive_statistics(stats_dict: Dict[str, Dict[str, float]]):
    """Print formatted descriptive statistics."""
    print("\n=== DESCRIPTIVE STATISTICS ===")
    for metric, stats in stats_dict.items():
        print(f"\n{metric}:")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Median: {stats['median']:.2f}")
        print(f"  Std Dev: {stats['std']:.2f}")
        print(f"  Min: {stats['min']:.2f}")
        print(f"  Max: {stats['max']:.2f}")
        print(f"  Q1: {stats['q1']:.2f}")
        print(f"  Q3: {stats['q3']:.2f}")
        print(f"  Count: {stats['count']}")


def analyze_data_distribution(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Analyze data distribution for each metric using statistical tests.
    
    Args:
        df: DataFrame containing server usage data
        
    Returns:
        Dictionary containing distribution analysis results
    """
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    distribution_results = {}
    
    for metric in metrics:
        if metric in df.columns:
            data = df[metric].dropna()
            
            # Shapiro-Wilk test for normality (works well for smaller samples)
            if len(data) <= 5000:
                shapiro_stat, shapiro_p = stats.shapiro(data)
            else:
                # Use Anderson-Darling test for larger samples
                shapiro_stat, shapiro_p = np.nan, np.nan
            
            # Kolmogorov-Smirnov test for normality
            ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
            
            # Skewness and Kurtosis
            skewness = stats.skew(data)
            kurtosis_val = stats.kurtosis(data)
            
            distribution_results[metric] = {
                'shapiro_statistic': shapiro_stat,
                'shapiro_p_value': shapiro_p,
                'ks_statistic': ks_stat,
                'ks_p_value': ks_p,
                'skewness': skewness,
                'kurtosis': kurtosis_val,
                'is_normal': shapiro_p > 0.05 if not np.isnan(shapiro_p) else ks_p > 0.05
            }
    
    return distribution_results


def print_distribution_analysis(dist_results: Dict[str, Dict[str, float]]):
    """Print formatted distribution analysis results."""
    print("\n=== DISTRIBUTION ANALYSIS ===")
    for metric, results in dist_results.items():
        print(f"\n{metric}:")
        if not np.isnan(results['shapiro_p_value']):
            print(f"  Shapiro-Wilk p-value: {results['shapiro_p_value']:.4f}")
        print(f"  KS test p-value: {results['ks_p_value']:.4f}")
        print(f"  Skewness: {results['skewness']:.4f}")
        print(f"  Kurtosis: {results['kurtosis']:.4f}")
        print(f"  Normal distribution: {'Yes' if results['is_normal'] else 'No'}")


def analyze_time_patterns(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Analyze performance patterns by time periods (hourly, daily patterns).
    
    Args:
        df: DataFrame containing server usage data
        
    Returns:
        Dictionary containing time-based analysis results
    """
    if 'Time' not in df.columns:
        raise ValueError("Time column not found in DataFrame")
    
    # Extract time components
    df = df.copy()
    df['Hour'] = df['Time'].dt.hour
    df['DayOfWeek'] = df['Time'].dt.dayofweek
    df['Date'] = df['Time'].dt.date
    
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    time_patterns = {}
    
    # Hourly patterns
    hourly_stats = df.groupby('Hour')[metrics].agg(['mean', 'max', 'std']).round(2)
    time_patterns['hourly'] = hourly_stats
    
    # Daily patterns (if multiple days)
    if df['Date'].nunique() > 1:
        daily_stats = df.groupby('Date')[metrics].agg(['mean', 'max', 'std']).round(2)
        time_patterns['daily'] = daily_stats
    
    return time_patterns


def calculate_alertness_thresholds(df: pd.DataFrame, method: str = 'percentile') -> Dict[str, Dict[str, float]]:
    """
    Calculate data-driven alertness thresholds for each metric.
    
    Args:
        df: DataFrame containing server usage data
        method: Method to calculate thresholds ('percentile', 'std', 'iqr')
        
    Returns:
        Dictionary containing threshold values for each metric
    """
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    thresholds = {}
    
    for metric in metrics:
        if metric in df.columns:
            data = df[metric].dropna()
            
            if method == 'percentile':
                # Use percentiles (90th and 95th percentile as warning and critical)
                thresholds[metric] = {
                    'warning': data.quantile(0.90),
                    'critical': data.quantile(0.95),
                    'method': 'percentile'
                }
            elif method == 'std':
                # Use standard deviation (mean + 2*std as warning, mean + 3*std as critical)
                mean_val = data.mean()
                std_val = data.std()
                thresholds[metric] = {
                    'warning': mean_val + 2 * std_val,
                    'critical': mean_val + 3 * std_val,
                    'method': 'standard_deviation'
                }
            elif method == 'iqr':
                # Use IQR method (Q3 + 1.5*IQR as warning, Q3 + 3*IQR as critical)
                q1 = data.quantile(0.25)
                q3 = data.quantile(0.75)
                iqr = q3 - q1
                thresholds[metric] = {
                    'warning': q3 + 1.5 * iqr,
                    'critical': q3 + 3 * iqr,
                    'method': 'iqr'
                }
    
    return thresholds


def detect_anomalies(df: pd.DataFrame, thresholds: Dict[str, Dict[str, float]]) -> Dict[str, pd.DataFrame]:
    """
    Detect anomalies based on calculated thresholds.
    
    Args:
        df: DataFrame containing server usage data
        thresholds: Dictionary containing threshold values
        
    Returns:
        Dictionary containing detected anomalies for each metric
    """
    anomalies = {}
    
    for metric, threshold_values in thresholds.items():
        if metric in df.columns:
            warning_threshold = threshold_values['warning']
            critical_threshold = threshold_values['critical']
            
            # Find anomalies
            warning_anomalies = df[df[metric] > warning_threshold].copy()
            critical_anomalies = df[df[metric] > critical_threshold].copy()
            
            anomalies[metric] = {
                'warning_count': len(warning_anomalies),
                'critical_count': len(critical_anomalies),
                'warning_data': warning_anomalies,
                'critical_data': critical_anomalies,
                'warning_percentage': (len(warning_anomalies) / len(df)) * 100,
                'critical_percentage': (len(critical_anomalies) / len(df)) * 100
            }
    
    return anomalies


def generate_optimization_recommendations(stats_dict: Dict[str, Dict[str, float]], 
                                       anomalies: Dict[str, Dict], 
                                       time_patterns: Dict[str, pd.DataFrame]) -> List[str]:
    """
    Generate concrete optimization recommendations based on analysis results.
    
    Args:
        stats_dict: Descriptive statistics
        anomalies: Detected anomalies
        time_patterns: Time-based analysis results
        
    Returns:
        List of optimization recommendations
    """
    recommendations = []
    
    # CPU Analysis
    if 'CPU_Usage' in stats_dict:
        cpu_stats = stats_dict['CPU_Usage']
        cpu_anomalies = anomalies.get('CPU_Usage', {})
        
        if cpu_stats['mean'] > 75:
            recommendations.append(
                f"🔴 HIGH CPU USAGE: Average CPU usage is {cpu_stats['mean']:.1f}%. "
                "Consider load balancing, process optimization, or hardware upgrades."
            )
        elif cpu_stats['mean'] > 60:
            recommendations.append(
                f"🟡 MODERATE CPU USAGE: Average CPU usage is {cpu_stats['mean']:.1f}%. "
                "Monitor peak hours and consider workload distribution."
            )
        
        if cpu_anomalies.get('critical_percentage', 0) > 5:
            recommendations.append(
                f"⚠️ CPU SPIKES: {cpu_anomalies['critical_percentage']:.1f}% of time shows critical CPU usage. "
                "Investigate resource-intensive processes during peak hours."
            )
    
    # Memory Analysis
    if 'Memory_Usage' in stats_dict:
        mem_stats = stats_dict['Memory_Usage']
        mem_anomalies = anomalies.get('Memory_Usage', {})
        
        if mem_stats['max'] > 15:
            recommendations.append(
                f"🔴 MEMORY CONCERN: Peak memory usage reaches {mem_stats['max']:.1f}GB. "
                "Consider memory optimization and garbage collection tuning."
            )
        
        if mem_stats['std'] > 2:
            recommendations.append(
                f"📊 MEMORY VARIABILITY: High memory usage variability (std: {mem_stats['std']:.1f}GB). "
                "Implement memory pooling and optimize application memory management."
            )
    
    # Network Analysis
    if 'Network_Usage' in stats_dict:
        net_stats = stats_dict['Network_Usage']
        
        if net_stats['max'] >= 200:
            recommendations.append(
                "🌐 NETWORK SATURATION: Network usage reaches maximum capacity. "
                "Consider bandwidth optimization, traffic shaping, or network upgrades."
            )
        
        if net_stats['mean'] > 150:
            recommendations.append(
                f"🌐 HIGH NETWORK USAGE: Average network usage is {net_stats['mean']:.1f}. "
                "Optimize data transfer protocols and implement caching strategies."
            )
    
    # Time-based recommendations
    if 'hourly' in time_patterns:
        hourly_data = time_patterns['hourly']
        if 'CPU_Usage' in hourly_data.columns.get_level_values(0):
            peak_hours = hourly_data[('CPU_Usage', 'mean')].nlargest(3).index.tolist()
            recommendations.append(
                f"⏰ PEAK HOURS IDENTIFIED: Highest CPU usage during hours {peak_hours}. "
                "Schedule intensive tasks outside these periods and implement auto-scaling."
            )
    
    # Temperature recommendations
    if 'Temperature' in stats_dict:
        temp_stats = stats_dict['Temperature']
        if temp_stats['max'] > 50:
            recommendations.append(
                f"🌡️ TEMPERATURE ALERT: Peak temperature reaches {temp_stats['max']:.1f}°C. "
                "Check cooling systems and ensure proper ventilation."
            )
    
    return recommendations


def run_complete_analysis(csv_path: str) -> None:
    """
    Run a complete analysis of server performance data.
    
    Args:
        csv_path: Path to the CSV file containing server data
    """
    print("🔍 Starting comprehensive server performance analysis...")
    
    # Load data
    df = load_csv(csv_path)
    print(f"✅ Loaded {len(df)} records from {csv_path}")
    
    # 1. Descriptive Statistics
    stats = calculate_descriptive_statistics(df)
    print_descriptive_statistics(stats)
    
    # 2. Distribution Analysis
    dist_analysis = analyze_data_distribution(df)
    print_distribution_analysis(dist_analysis)
    
    # 3. Time Pattern Analysis
    time_patterns = analyze_time_patterns(df)
    print("\n=== TIME PATTERN ANALYSIS ===")
    if 'hourly' in time_patterns:
        print("\nHourly CPU Usage Patterns:")
        print(time_patterns['hourly'][('CPU_Usage', 'mean')].round(2))
    
    # 4. Threshold Calculation and Anomaly Detection
    thresholds = calculate_alertness_thresholds(df, method='percentile')
    anomalies = detect_anomalies(df, thresholds)
    
    print("\n=== ALERTNESS THRESHOLDS ===")
    for metric, threshold in thresholds.items():
        print(f"{metric}: Warning={threshold['warning']:.2f}, Critical={threshold['critical']:.2f}")
    
    print("\n=== ANOMALY DETECTION ===")
    for metric, anomaly_data in anomalies.items():
        print(f"{metric}: {anomaly_data['warning_count']} warnings, {anomaly_data['critical_count']} critical alerts")
    
    # 5. Generate Recommendations
    recommendations = generate_optimization_recommendations(stats, anomalies, time_patterns)
    print("\n=== OPTIMIZATION RECOMMENDATIONS ===")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    # 6. Create Visualizations
    print(f"\n📊 Generating performance visualizations in data/plot/...")
    generate_all_visualizations(df, time_patterns, thresholds, anomalies, "data/plot")
    
    print("\n✅ Analysis complete! Check the generated plots in data/plot/ for visual insights.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze server performance data")
    parser.add_argument("--csv", default="data/server_usage_data.csv", help="Path to CSV file")
    args = parser.parse_args()
    
    run_complete_analysis(args.csv)
