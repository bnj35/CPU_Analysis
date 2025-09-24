from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional


def create_performance_visualizations(df: pd.DataFrame, output_dir: str = "data/plot", save_plots: bool = True):
    """
    Create visualizations for performance analysis.
    
    Args:
        df: DataFrame containing server usage data
        output_dir: Directory to save plot files
        save_plots: Whether to save plots to files
    """
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    
    # 1. Time series plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Server Performance Metrics Over Time', fontsize=16)
    
    for i, metric in enumerate(metrics):
        if metric in df.columns:
            ax = axes[i//2, i%2]
            ax.plot(df['Time'], df[metric], alpha=0.7)
            ax.set_title(f'{metric} Over Time')
            ax.set_ylabel(metric)
            ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    if save_plots:
        plt.savefig(output_path / 'performance_timeseries.png', dpi=300, bbox_inches='tight')
    
    
    # 2. Distribution plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Distribution of Performance Metrics', fontsize=16)
    
    for i, metric in enumerate(metrics):
        if metric in df.columns:
            ax = axes[i//2, i%2]
            ax.hist(df[metric], bins=30, alpha=0.7, edgecolor='black')
            ax.set_title(f'{metric} Distribution')
            ax.set_xlabel(metric)
            ax.set_ylabel('Frequency')
    
    plt.tight_layout()
    if save_plots:
        plt.savefig(output_path / 'performance_distributions.png', dpi=300, bbox_inches='tight')
    
    
    # 3. Correlation heatmap
    correlation_matrix = df[metrics].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Performance Metrics')
    if save_plots:
        plt.savefig(output_path / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
    


def create_hourly_pattern_plot(time_patterns: dict, output_dir: str = "data/plot", save_plots: bool = True):
    """
    Create visualization for hourly usage patterns.
    
    Args:
        time_patterns: Dictionary containing time-based analysis results
        output_dir: Directory to save plot files
        save_plots: Whether to save plots to files
    """
    if 'hourly' not in time_patterns:
        print("No hourly data available for plotting")
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    hourly_data = time_patterns['hourly']
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Hourly Performance Patterns', fontsize=16)
    
    for i, metric in enumerate(metrics):
        if metric in hourly_data.columns.get_level_values(0):
            ax = axes[i//2, i%2]
            hours = hourly_data.index
            mean_values = hourly_data[(metric, 'mean')]
            
            ax.plot(hours, mean_values, marker='o', linewidth=2, markersize=4)
            ax.set_title(f'Average {metric} by Hour')
            ax.set_xlabel('Hour of Day')
            ax.set_ylabel(f'{metric} (Average)')
            ax.grid(True, alpha=0.3)
            ax.set_xticks(range(0, 24, 2))
    
    plt.tight_layout()
    if save_plots:
        plt.savefig(output_path / 'hourly_patterns.png', dpi=300, bbox_inches='tight')
    


def create_anomaly_visualization(df: pd.DataFrame, thresholds: dict, anomalies: dict, 
                               output_dir: str = "data/plot", save_plots: bool = True):
    """
    Create visualization highlighting anomalies and thresholds.
    
    Args:
        df: DataFrame containing server usage data
        thresholds: Dictionary containing threshold values
        anomalies: Dictionary containing detected anomalies
        output_dir: Directory to save plot files
        save_plots: Whether to save plots to files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Performance Metrics with Anomaly Detection', fontsize=16)
    
    for i, metric in enumerate(metrics):
        if metric in df.columns and metric in thresholds:
            ax = axes[i//2, i%2]
            
            # Plot the time series
            ax.plot(df['Time'], df[metric], alpha=0.6, color='blue', label=metric)
            
            # Add threshold lines
            warning_threshold = thresholds[metric]['warning']
            critical_threshold = thresholds[metric]['critical']
            
            ax.axhline(y=warning_threshold, color='orange', linestyle='--', 
                      label=f'Warning ({warning_threshold:.1f})')
            ax.axhline(y=critical_threshold, color='red', linestyle='--', 
                      label=f'Critical ({critical_threshold:.1f})')
            
            # Highlight anomalies
            if metric in anomalies:
                critical_data = anomalies[metric]['critical_data']
                if len(critical_data) > 0:
                    ax.scatter(critical_data['Time'], critical_data[metric], 
                             color='red', s=10, alpha=0.8, label='Critical Anomalies')
            
            ax.set_title(f'{metric} with Thresholds')
            ax.set_ylabel(metric)
            ax.legend(fontsize=8)
            ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    if save_plots:
        plt.savefig(output_path / 'anomaly_detection.png', dpi=300, bbox_inches='tight')



def generate_all_visualizations(df: pd.DataFrame, time_patterns: dict, thresholds: dict, 
                              anomalies: dict, output_dir: str = "data/plot"):
    """
    Generate all visualization plots and save them to the specified directory.
    
    Args:
        df: DataFrame containing server usage data
        time_patterns: Dictionary containing time-based analysis results
        thresholds: Dictionary containing threshold values
        anomalies: Dictionary containing detected anomalies
        output_dir: Directory to save plot files
    """
    print(f"📊 Generating performance visualizations in {output_dir}...")
    
    # Create main performance visualizations
    create_performance_visualizations(df, output_dir)
    
    # Create hourly pattern plots
    create_hourly_pattern_plot(time_patterns, output_dir)
    
    # Create anomaly detection plots
    create_anomaly_visualization(df, thresholds, anomalies, output_dir)
    
    print(f"✅ All visualizations saved to {output_dir}/")