import pandas as pd
import numpy as np

class AlphaEngine:
    def __init__(self, data):
        self.data = data
        
    def calculate_cfo_ratio(self):
        """Calculate CFO to Market Cap ratio"""
        self.data['cfo_ratio'] = self.data['cfo'] / self.data['market_cap']
        return self.data
        
    def calculate_ranks(self):
        """Calculate industry relative ranks"""
        self.data['industry_rank'] = self.data.groupby('industry')['cfo_ratio'].rank(pct=True)
        return self.data
        
    def generate_signals(self, threshold=0.8):
        """Generate trading signals"""
        self.calculate_cfo_ratio()
        self.calculate_ranks()
        return self.data[self.data['industry_rank'] > threshold]