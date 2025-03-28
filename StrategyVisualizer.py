import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class StrategyVisualizer:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")

    def plot_cfo_ratio_distribution(self, signals):
        """Plot distribution of CFO ratios"""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=signals, x='cfo_ratio', hue='industry', multiple="stack")
        plt.title('Distribution of CFO/Market Cap Ratios by Industry')
        plt.xlabel('CFO/Market Cap Ratio')
        plt.ylabel('Count')
        plt.savefig(f'{self.data_dir}/cfo_distribution.png')
        plt.close()

    def plot_industry_rankings(self, signals):
        """Plot industry rankings"""
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=signals, x='industry', y='industry_rank')
        plt.xticks(rotation=45)
        plt.title('Industry Rankings Distribution')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/industry_rankings.png')
        plt.close()

    def plot_top_stocks(self, signals, top_n=10):
        """Plot top stocks by CFO ratio"""
        top_stocks = signals.nlargest(top_n, 'cfo_ratio')
        plt.figure(figsize=(12, 6))
        sns.barplot(data=top_stocks, x=top_stocks.index, y='cfo_ratio')
        plt.xticks(rotation=45)
        plt.title(f'Top {top_n} Stocks by CFO/Market Cap Ratio')
        plt.tight_layout()
        plt.savefig(f'{self.data_dir}/top_stocks.png')
        plt.close()