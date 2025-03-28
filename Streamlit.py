import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

def fetch_data(tickers):
    data = {}
    progress_bar = st.progress(0)
    for i, ticker in enumerate(tickers):
        try:
            stock = yf.Ticker(ticker)
            data[ticker] = {
                'cfo': stock.info.get('operatingCashflow'),
                'market_cap': stock.info.get('marketCap'),
                'industry': stock.info.get('industry')
            }
            progress_bar.progress((i + 1) / len(tickers))
        except Exception as e:
            st.error(f"Error fetching {ticker}: {e}")
    return pd.DataFrame.from_dict(data, orient='index')

def calculate_alpha(df):
    df['cfo_ratio'] = df['cfo'] / df['market_cap']
    df['industry_rank'] = df.groupby('industry')['cfo_ratio'].rank(pct=True)
    return df

def main():
    st.title("CFO Alpha Strategy Dashboard")
    
    # Sidebar
    st.sidebar.header("Settings")
    default_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    tickers = st.sidebar.text_area("Enter stock tickers (one per line)", 
                                 "\n".join(default_tickers)).split()
    
    if st.sidebar.button("Run Analysis"):
        # Fetch and process data
        with st.spinner("Fetching data..."):
            df = fetch_data(tickers)
            signals = calculate_alpha(df)
            
        # Display results in tabs
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Charts", "📑 Data"])
        
        with tab1:
            st.header("Top Ranked Stocks")
            st.dataframe(signals.sort_values('industry_rank', ascending=False))
        
        with tab2:
            # CFO Ratio Plot
            st.subheader("CFO/Market Cap Ratio by Company")
            fig1 = px.bar(signals, 
                         x=signals.index, 
                         y='cfo_ratio',
                         color='industry',
                         title='CFO Ratio by Company')
            st.plotly_chart(fig1)
            
            # Industry Rankings
            st.subheader("Industry Rankings Distribution")
            fig2 = px.box(signals, 
                         x='industry', 
                         y='industry_rank',
                         title='Industry Rankings Distribution')
            st.plotly_chart(fig2)
        
        with tab3:
            st.header("Raw Data")
            st.dataframe(signals)
            
            # Download button
            csv = signals.to_csv()
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='cfo_alpha_signals.csv',
                mime='text/csv',
            )

if __name__ == "__main__":
    main()