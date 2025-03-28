import os
import pandas as pd
from dotenv import load_dotenv
import yfinance as yf
from StrategyVisualizer import StrategyVisualizer

# Add directory creation function
def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def fetch_data(tickers):
    """Fetch stock data using yfinance"""
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data[ticker] = {
                'cfo': stock.info.get('operatingCashflow'),
                'market_cap': stock.info.get('marketCap'),
                'industry': stock.info.get('industry')
            }
            print(f"Successfully fetched data for {ticker}")
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
    return pd.DataFrame.from_dict(data, orient='index')

def calculate_alpha(df):
    """Calculate CFO/Market Cap ratio and rank within industry"""
    df['cfo_ratio'] = df['cfo'] / df['market_cap']
    df['industry_rank'] = df.groupby('industry')['cfo_ratio'].rank(pct=True)
    return df

def main():
    # Ensure data directory exists
    data_dir = ensure_data_dir()
    
    # Initialize visualizer
    visualizer = StrategyVisualizer(data_dir)
    
    # Sample universe of stocks (expanded)
    universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 
                'NVDA', 'JPM', 'V', 'WMT', 'JNJ', 
                'PG', 'XOM', 'BAC', 'HD', 'CVX']
    
    # Fetch data
    print("Fetching data...")
    df = fetch_data(universe)
    
    # Calculate alpha signals
    print("Calculating signals...")
    signals = calculate_alpha(df)
    
    # Generate visualizations
    print("Generating visualizations...")
    visualizer.plot_cfo_ratio_distribution(signals)
    visualizer.plot_industry_rankings(signals)
    visualizer.plot_top_stocks(signals)
    
    # Save results
    output_path = os.path.join(data_dir, 'signals.csv')
    signals.to_csv(output_path)
    print(f"Results saved to {output_path}")
    
    # Display top signals
    print("\nTop signals:")
    print(signals.sort_values('industry_rank', ascending=False))

if __name__ == '__main__':
    main()