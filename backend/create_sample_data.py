import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_sample_data():
    """Create sample market data for testing"""
    
    # Create data directory if it doesn't exist
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate sample date range (last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Remove weekends
    dates = [d for d in dates if d.weekday() < 5]
    
    # Generate sample ACWI data
    np.random.seed(42)  # For reproducible results
    
    # ACWI sample data
    acwi_base_price = 100
    acwi_prices = [acwi_base_price]
    
    for i in range(1, len(dates)):
        # Random walk with slight upward bias
        change = np.random.normal(0.001, 0.015)  # 0.1% daily return, 1.5% volatility
        new_price = acwi_prices[-1] * (1 + change)
        acwi_prices.append(new_price)
    
    # Create ACWI DataFrame
    acwi_data = pd.DataFrame({
        'Open': [p * (1 + np.random.normal(0, 0.002)) for p in acwi_prices],
        'High': [p * (1 + abs(np.random.normal(0.005, 0.003))) for p in acwi_prices],
        'Low': [p * (1 - abs(np.random.normal(0.005, 0.003))) for p in acwi_prices],
        'Close': acwi_prices,
        'Volume': [np.random.randint(1000000, 5000000) for _ in acwi_prices]
    }, index=dates[:len(acwi_prices)])
    
    # S&P 500 sample data
    np.random.seed(24)  # Different seed for S&P
    sp500_base_price = 4000
    sp500_prices = [sp500_base_price]
    
    for i in range(1, len(dates)):
        # Random walk with slight upward bias
        change = np.random.normal(0.0012, 0.018)  # 0.12% daily return, 1.8% volatility
        new_price = sp500_prices[-1] * (1 + change)
        sp500_prices.append(new_price)
    
    # Create S&P 500 DataFrame
    sp500_data = pd.DataFrame({
        'Open': [p * (1 + np.random.normal(0, 0.002)) for p in sp500_prices],
        'High': [p * (1 + abs(np.random.normal(0.006, 0.004))) for p in sp500_prices],
        'Low': [p * (1 - abs(np.random.normal(0.006, 0.004))) for p in sp500_prices],
        'Close': sp500_prices,
        'Volume': [np.random.randint(3000000, 8000000) for _ in sp500_prices]
    }, index=dates[:len(sp500_prices)])
    
    # Save to CSV files
    acwi_file = os.path.join(data_dir, "acwi.csv")
    sp500_file = os.path.join(data_dir, "sp500.csv")
    
    acwi_data.to_csv(acwi_file)
    sp500_data.to_csv(sp500_file)
    
    print(f"✅ Created sample ACWI data: {acwi_file} ({len(acwi_data)} rows)")
    print(f"✅ Created sample S&P 500 data: {sp500_file} ({len(sp500_data)} rows)")
    
    # Print some summary stats
    print("\n📊 Sample Data Summary:")
    print(f"ACWI - Start: ${acwi_data['Close'].iloc[0]:.2f}, End: ${acwi_data['Close'].iloc[-1]:.2f}")
    print(f"S&P 500 - Start: ${sp500_data['Close'].iloc[0]:.2f}, End: ${sp500_data['Close'].iloc[-1]:.2f}")
    
    return {
        "acwi_file": acwi_file,
        "sp500_file": sp500_file,
        "acwi_data": acwi_data,
        "sp500_data": sp500_data
    }

if __name__ == "__main__":
    # Create sample data
    result = create_sample_data()
    print("\nSample data created successfully!")