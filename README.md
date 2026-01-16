# Square Cafe Report

A desktop application for pulling specific metrics from Square API for cafe managers.

## Features

- **Longest Ticket Time**: Track the longest ticket time between 11am-2pm PST
- **Average Ticket Length**: Calculate average ticket length for the entire day
- **Sales Breakdown**: View daily sales with top 5 drinks breakdown
- **Multi-Location Support**: Select between different cafe locations

## Requirements

- Python 3.8+
- Square API credentials (Access Token)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `config.example.yaml` to `config.yaml`
2. Add your Square API access token and location IDs
3. Run the application: `streamlit run app.py`

## Usage

1. Launch the application
2. Select your cafe location from the dropdown
3. Choose the date for the report
4. View the metrics in the interactive dashboard

## Tech Stack

- **Python**: Core language
- **Streamlit**: Interactive dashboard UI
- **Square Python SDK**: Square API integration
- **Pandas**: Data processing and analysis
