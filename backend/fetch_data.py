import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, Any

def fetch_market_data() -> Dict[str, Any]:
    """
    Fetch ACWI and S&P 500 market data using yfinance
    
    Returns:
        dict: Status and file information
    """
    try:
        # Create data directory if it doesn't exist
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Define tickers
        tickers = {
            "ACWI": "ACWI",  # iShares MSCI ACWI ETF
            "SP500": "^GSPC"  # S&P 500 Index
        }
        
        # Calculate date range (get 2 years of data to ensure we have enough)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # ~2 years
        
        files_created = []
        
        for name, ticker in tickers.items():
            print(f"Fetching data for {name} ({ticker})...")
            
            # Fetch data
            stock = yf.Ticker(ticker)
            data = stock.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                interval="1d"
            )
            
            if data.empty:
                raise Exception(f"No data found for {ticker}")
            
            # Save to CSV
            filename = f"{name.lower()}.csv"
            filepath = os.path.join(data_dir, filename)
            data.to_csv(filepath)
            files_created.append(filepath)
            
            print(f"✅ Saved {name} data to {filepath} ({len(data)} rows)")
        
        return {
            "status": "success",
            "files": files_created,
            "message": f"Successfully fetched data for {len(tickers)} instruments"
        }
        
    except Exception as e:
        raise Exception(f"Error fetching market data: {str(e)}")

if __name__ == "__main__":
    # Test the function
    result = fetch_market_data()
    print("\nFetch Data Result:")
    print(result)