import pprint
import random
import time

import numpy as np
import pandas as pd
import requests

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 5000)


class NSE:
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

        self.session = requests.Session()
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def pre_market_data(self, category):
        pre_market_category = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME",
                               "FO": "FO", "Others": "OTHERS", "All": "ALL"}
        category = category.upper()
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 to 4 seconds
        time.sleep(delay_before_display)

        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key="
                                f"{pre_market_category[category]}", headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        df = pd.DataFrame(new_data)
        df = df.drop(
            ["identifier", "purpose", "identifier", "yearHigh", "yearLow", "marketCap", "iep", "chartTodayPath"],
            axis=1)
        df = df.drop(0)
        df = df.sort_values(by="finalQuantity", ascending=False)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        return df

    def equity_market_data(self, category, symbol_list=False):
        category = category.upper().replace(' ', '%20').replace('&', '%26')
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 to 4 seconds
        time.sleep(delay_before_display)
        data = self.session.get(f"https://www.nseindia.com/api/equity-stockIndices?index={category}",
                                headers=self.headers).json()["data"]
        df = pd.DataFrame(data)
        df = df.drop(
            ["meta", "priority", "identifier", "yearHigh", "yearLow", "ffmc", "nearWKH", "nearWKL", "perChange365d",
             "date365dAgo", "chart365dPath", "date30dAgo", "perChange30d", "chart30dPath", "series", "chartTodayPath"],
            axis=1)
        df = df.drop(0)
        df = df.sort_values(by="totalTradedVolume", ascending=False)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        if symbol_list:
            return list(df.index)
        else:
            return df

    def indices_data(self):
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 to 4 seconds
        time.sleep(delay_before_display)

        data = self.session.get(f"https://www.nseindia.com/api/allIndices",
                                headers=self.headers).json()["data"]
        df = pd.DataFrame(data)
        df = df.drop(
            ["key", "index", "variation", "yearHigh", "yearLow", "pe", "pb", "dy", "perChange365d", "date365dAgo",
             "chart365dPath", "date30dAgo", "perChange30d", "chart30dPath", "oneWeekAgo", "oneMonthAgo", "oneYearAgo",
             "chartTodayPath"], axis=1)
        indicestodrop = [54, 17, 42, 6, 11, 52, 12, 21, 51, 9, 39, 40, 7, 32, 13, 14, 44, 10, 1, 71, 72, 66, 67, 69, 70,
                         1, 41, 68, 4, 5, 48, 3, 49, 47, 57, 50, 2, 64, 62, 43, 36, 46, 45, 33, 58, 35, 65, 38, 37, 30,
                         63, 31, 53, 34, 8, 59, 16, 56, 61, 59, 61, 16, 56]
        df = df.drop(indicestodrop)
        # df = df.set_index("indexSymbol", drop=True)
        df = df.sort_values(by="percentChange", ascending=False)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        return df

    def about_holidays(self, category):
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 to 4 seconds
        time.sleep(delay_before_display)
        data = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={category.lower()}',
                                headers=self.headers).json()
        df = pd.DataFrame(list(data.values())[0])
        return df

    def equity_info(self, symbol, trade_info=False):
        # Introduce random delay before displaying the chart
        delay_before_display = random.uniform(1, 6)  # Random delay between 1 to 4 seconds
        time.sleep(delay_before_display)
        symbol = symbol.replace(' ', '%20').replace('&', '%26')
        url = ('https://www.nseindia.com/api/quote-equity?symbol=' + symbol +
               ("&section=trade_info" if trade_info else ""))
        data = self.session.get(url, headers=self.headers).json()
        return data
