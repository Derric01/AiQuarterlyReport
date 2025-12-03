import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Dict, Any

def load_market_data() -> Dict[str, pd.DataFrame]:
    """Load market data from CSV files"""
    data_files = {
        "acwi": "data/acwi.csv",
        "sp500": "data/sp500.csv"
    }
    
    datasets = {}
    for name, filepath in data_files.items():
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}. Please run fetch data first.")
        
        # Read CSV without parsing dates first
        df = pd.read_csv(filepath)
        # Parse dates manually to handle timezone properly
        df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
        df.set_index('Date', inplace=True)
        datasets[name] = df
        
    return datasets

def get_quarter_dates(quarter_offset: int = 0) -> tuple:
    """
    Get start and end dates for a specific quarter
    
    Args:
        quarter_offset: 0 for current quarter, -1 for previous quarter, etc.
    
    Returns:
        tuple: (start_date, end_date)
    """
    today = datetime.now()
    
    # Determine current quarter
    current_quarter = (today.month - 1) // 3 + 1
    current_year = today.year
    
    # Adjust for offset
    target_quarter = current_quarter + quarter_offset
    target_year = current_year
    
    while target_quarter <= 0:
        target_quarter += 4
        target_year -= 1
    
    while target_quarter > 4:
        target_quarter -= 4
        target_year += 1
    
    # Calculate quarter start and end dates
    quarter_starts = {
        1: (1, 1),   # Q1: Jan-Mar
        2: (4, 1),   # Q2: Apr-Jun  
        3: (7, 1),   # Q3: Jul-Sep
        4: (10, 1),  # Q4: Oct-Dec
    }
    
    start_month, start_day = quarter_starts[target_quarter]
    start_date = datetime(target_year, start_month, start_day)
    
    # End date is start of next quarter minus 1 day
    if target_quarter == 4:
        end_date = datetime(target_year + 1, 1, 1) - timedelta(days=1)
    else:
        next_month, _ = quarter_starts[target_quarter + 1]
        end_date = datetime(target_year, next_month, 1) - timedelta(days=1)
    
    return start_date, end_date

def calculate_return(data: pd.DataFrame, start_date: datetime, end_date: datetime) -> float:
    """Calculate return between two dates"""
    # Now that data is timezone-naive, we can do direct comparison
    mask = (data.index >= start_date) & (data.index <= end_date)
    period_data = data[mask]
    
    if len(period_data) < 2:
        return 0.0
    
    start_price = period_data['Close'].iloc[0]
    end_price = period_data['Close'].iloc[-1]
    
    return ((end_price - start_price) / start_price) * 100

def count_new_highs(data: pd.DataFrame, start_date: datetime, end_date: datetime) -> int:
    """Count number of new highs during the period"""
    # Now that data is timezone-naive, we can do direct comparison
    period_data = data[(data.index >= start_date) & (data.index <= end_date)]
    
    if len(period_data) == 0:
        return 0
    
    new_highs = 0
    running_max = period_data['High'].iloc[0]
    
    for high in period_data['High']:
        if high > running_max:
            new_highs += 1
            running_max = high
    
    return new_highs

def compute_quarterly_metrics() -> Dict[str, Any]:
    """
    Compute quarterly financial metrics
    
    Returns:
        dict: Computed metrics
    """
    try:
        # Load market data
        datasets = load_market_data()
        acwi_data = datasets["acwi"]
        sp500_data = datasets["sp500"]
        
        # Get date ranges
        q_start, q_end = get_quarter_dates(-1)  # Previous completed quarter
        ytd_start = datetime(q_end.year, 1, 1)  # Year to date
        
        print(f"Computing metrics for Q{((q_start.month - 1) // 3) + 1} {q_start.year}")
        print(f"Quarter: {q_start.date()} to {q_end.date()}")
        print(f"YTD: {ytd_start.date()} to {q_end.date()}")
        
        # Calculate quarterly returns
        acwi_quarter_return = calculate_return(acwi_data, q_start, q_end)
        sp500_quarter_return = calculate_return(sp500_data, q_start, q_end)
        
        # Calculate YTD returns
        acwi_ytd_return = calculate_return(acwi_data, ytd_start, q_end)
        sp500_ytd_return = calculate_return(sp500_data, ytd_start, q_end)
        
        # Count new highs
        acwi_new_highs = count_new_highs(acwi_data, q_start, q_end)
        sp500_new_highs = count_new_highs(sp500_data, q_start, q_end)
        
        metrics = {
            "acwi_quarter_return": round(acwi_quarter_return, 2),
            "sp500_quarter_return": round(sp500_quarter_return, 2),
            "acwi_ytd_return": round(acwi_ytd_return, 2),
            "sp500_ytd_return": round(sp500_ytd_return, 2),
            "acwi_new_highs": acwi_new_highs,
            "sp500_new_highs": sp500_new_highs,
            "quarter": f"Q{((q_start.month - 1) // 3) + 1} {q_start.year}",
            "period_start": q_start.strftime("%Y-%m-%d"),
            "period_end": q_end.strftime("%Y-%m-%d")
        }
        
        print("\n📊 Computed Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
        return metrics
        
    except Exception as e:
        raise Exception(f"Error computing metrics: {str(e)}")

if __name__ == "__main__":
    # Test the function
    try:
        metrics = compute_quarterly_metrics()
        print("\nMetrics Result:")
        print(metrics)
    except Exception as e:
        print(f"Error: {e}")