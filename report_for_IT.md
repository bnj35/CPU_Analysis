# Server Analysis Report — OPTIMAL

Date: September 24, 2025  
Author: Emma (automated analysis)

## 1. Executive Summary

An analysis of server performance metrics (`CPU_Usage`, `Memory_Usage`, `Network_Usage`, `Temperature`) was conducted using data collected from the file `data/server_usage_data.csv`. Key findings:

- Average CPU usage: ~41.4% (std dev ≈ 20.6) with peaks at 100%.  
- Average memory usage: ~7.2 GB, peak at 16 GB, significant variability (std dev ≈ 3.2 GB).  
- Average network usage: ~115 (unit), peak at 200 (maximum observed capacity).  
- Average temperature: ~41.4°C, peak at ~57.9°C.  

Data-driven alert thresholds (90th/95th percentiles) were calculated, and anomalies were detected. Results indicate periods of high load (peak hours) and risks of network saturation and overheating.

---

## 2. Key Figures

- Number of records analyzed: **10,080**

Main statistics:

| Metric          | Average | Median | Std Dev | Min  | Max  | Q1   | Q3   |
|------------------|--------:|-------:|--------:|-----:|-----:|-----:|-----:|
| CPU_Usage (%)    |  41.41  |  39.18 |  20.59  |  10  | 100  | 25.63| 55.39|
| Memory_Usage (GB)|   7.20  |   7.14 |   3.22  |   2  |  16  |  4.79|  9.04|
| Network_Usage    | 115.01  | 108.46 |  53.87  |  25  | 200  | 74.55|159.78|
| Temperature (°C) |  41.37  |  40.81 |   6.51  | 27.80| 57.86| 36.24| 46.80|

Thresholds (90th/95th percentile method):

- CPU: Warning = 69.20%, Critical = 78.57%  
- Memory: Warning = 11.76 GB, Critical = 12.66 GB  
- Network: Warning = 198.97, Critical = 200.00  
- Temperature: Warning = 50.10°C, Critical = 51.81°C  

Detected anomalies (default method): approximately **10% warnings** and **5% critical** (aligned with chosen percentiles).

---

## 3. Detailed Observations

- **CPU**
    - Moderate average but high variability (high std dev). Regular peaks (7:00 and 1:00). Possible nightly batch jobs or scheduled tasks.  
    - Immediate recommendation: investigate processes triggered around 1:00 and morning (7-8 AM); consider rescheduling or increasing capacity.

- **Memory**
    - Significant peaks (up to 16 GB). High variability → potential memory leaks or resource-intensive applications.  
    - Recommendation: audit memory-consuming applications; consider containerization to isolate peaks.

- **Network**
    - Usage reaching maximum observed capacity (200); risk of saturation. No strict critical detected (depends on comparator), but frequent warnings.  
    - Recommendation: monitor packet loss and latency; consider upgrades if traffic remains high.

- **Temperature**
    - Peaks >50°C (max ≈ 57.9°C). Possible correlation with CPU peaks.  
    - Recommendation: inspect cooling (airflow), check sensors, alert above 50°C in production.

---

## 4. Operational Recommendations (Prioritized)

**Short Term (Immediate)**  
     - Define operational alerts with 90/95% thresholds; adjust if too noisy.  
     - Schedule investigation of tasks around 1:00 and 7:00 — identify heavy processes.  
     - Set temperature alerts (>50°C) and inspect cooling systems.

---