# Parameter Visualization App

A web-based tool for visualizing parameter history data from Excel files.

## Features

- Upload Excel files containing parameter data
- Automatic visualization of key metrics:
  - Average Force over time
  - Instantaneous Slope
  - Average Slope
  - Total Work (cumulative energy)
- Custom graph creator with multi-parameter selection
- Interactive plots with Plotly

## Requirements

- streamlit
- pandas
- plotly
- openpyxl

## Usage

1. Run the application:
```
streamlit run gorsellestirme_app.py
```

2. Upload your Excel file containing parameter history

3. View automatically generated graphs or create custom visualizations

## File Format

The Excel file should contain the following columns:
- Zaman (Kümülatif) - Cumulative Time
- Ortalama Kuvvet (N) - Average Force
- Anlik_Eğim (O anki) - Instantaneous Slope
- Ortalama Eğim (N/s) - Average Slope
- Toplam İş (J) [K-Y Alanı] - Total Work
