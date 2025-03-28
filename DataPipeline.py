import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import time
import logging

class DataPipeline:
    def __init__(self, api_key):
        self.av_client = TimeSeries(key=api_key)
        self.logger = logging.getLogger(__name__)
        
    def fetch_fundamentals(self, ticker):
        """Fetch fundamental data for a given ticker"""
        try:
            # Get cash flow data
            cf_data = self.av_client.get_cash_flow_annual(ticker)[0]
            operating_cashflow = cf_data.get('operatingCashflow', None)
            
            # Get company overview for market cap
            overview = self.av_client.get_company_overview(ticker)[0]
            market_cap = overview.get('MarketCapitalization', None)
            industry = overview.get('Industry', None)
            
            return {
                'cfo': operating_cashflow,
                'market_cap': market_cap,
                'industry': industry
            }
        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
            
    def process_universe(self, tickers):
        """Process entire universe of stocks"""
        data = []
        for ticker in tickers:
            fundamentals = self.fetch_fundamentals(ticker)
            if fundamentals:
                fundamentals['ticker'] = ticker
                data.append(fundamentals)
            time.sleep(12)  # API rate limiting
            
        return pd.DataFrame(data)