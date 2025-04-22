# CSV Database Assessment Tool

A Streamlit application that analyzes CSV files and generates assessment reports with reliability metrics.

## Features

- Upload CSV files for analysis
- View summary statistics (rows, data points)
- Generate detailed column analysis with reliability metrics
- Download formatted Excel reports

## Metrics Calculated

- **Total percentage**: Percentage of filled data points for each column
- **Positive Share**: Number of filled cells in each column
- **Positive Reliability**: Random value between 90-100 (if positive share > 0)
- **Negative Share**: Number of empty cells in each column
- **Negative Reliability**: Random value between 90-100 (if negative share > 0)
- **Reliability Percentage**: Average of positive and negative reliability

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd csv-analyzer
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
streamlit run app.py
```

## Usage

1. Open the application in your web browser (default: http://localhost:8501)
2. Upload a CSV file using the file uploader
3. View the analysis results
4. Download the Excel report with the "Download Excel Report" button

## Excel Report Format

The downloaded Excel report follows these formatting guidelines:
- Font: Roboto, Size 10
- Text alignment: Center (Left for column names)
- Header row: Background color #0B5394, white text
- Percentage values include the '%' symbol

## Requirements

- Python 3.6+
- pandas
- streamlit
- openpyxl
- XlsxWriter

## Sample Data

A sample CSV file is included in the repository for testing purposes.
