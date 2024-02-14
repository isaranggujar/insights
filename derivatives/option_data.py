import random
import time

import pandas as pd
import requests

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 5000)

indices_list = ['NIFTY', 'FINNIFTY', 'BANKNIFTY', 'MIDCPNIFTY']


class NSE:
    def __init__(self):
        self.headers = {
            'Accept': '* / *',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

        self.session = requests.Session()
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def get_nse_option_chain(self, symbol):
        if any(x in symbol for x in indices_list):
            data = self.session.get(f"https://www.nseindia.com/api/option-chain-indices?symbol="
                                    f"{symbol}", headers=self.headers)
        else:
            data = self.session.get(f"https://www.nseindia.com/api/option-chain-equities?symbol=" + f"{symbol}",
                                    headers=self.headers)
        return data

    def nse_live_option_chain(self, symbol: str, expiry_date: str = None, oi_mode: str = "compact"):
        """
        get live nse option chain.
        :param symbol: eg:SBIN/BANKNIFTY
        :param expiry_date: '01-06-2023'
        :param oi_mode: eg: full/compact
        :return: pands dataframe
        """
        # Introduce random delay before making the request
        delay = random.uniform(1, 6)  # Random delay between 2 to 6 seconds
        time.sleep(delay)

        payload = nse.get_nse_option_chain(symbol).json()
        if expiry_date:
            exp_date = pd.to_datetime(expiry_date, format='%d-%m-%Y')
            expiry_date = exp_date.strftime('%d-%b-%Y')

        if oi_mode == 'compact':
            col_names = ['Fetch_Time', 'Symbol', 'Expiry_Date', 'CALLS_OI', 'CALLS_Chng_in_OI', 'CALLS_Volume',
                         'CALLS_IV',
                         'CALLS_LTP', 'CALLS_Net_Chng', 'Strike_Price', 'PUTS_OI', 'PUTS_Chng_in_OI', 'PUTS_Volume',
                         'PUTS_IV', 'PUTS_LTP', 'PUTS_Net_Chng']
        else:
            col_names = ['Fetch_Time', 'Symbol', 'Expiry_Date', 'CALLS_OI', 'CALLS_Chng_in_OI', 'CALLS_Volume',
                         'CALLS_IV',
                         'CALLS_LTP', 'CALLS_Net_Chng', 'CALLS_Bid_Qty', 'CALLS_Bid_Price', 'CALLS_Ask_Price',
                         'CALLS_Ask_Qty', 'Strike_Price', 'PUTS_Bid_Qty', 'PUTS_Bid_Price', 'PUTS_Ask_Price',
                         'PUTS_Ask_Qty',
                         'PUTS_Net_Chng', 'PUTS_LTP', 'PUTS_IV', 'PUTS_Volume', 'PUTS_Chng_in_OI', 'PUTS_OI']

        oi_data = pd.DataFrame(columns=col_names)

        oi_row = {'Fetch_Time': None, 'Symbol': None, 'Expiry_Date': None, 'CALLS_OI': 0, 'CALLS_Chng_in_OI': 0,
                  'CALLS_Volume': 0,
                  'CALLS_IV': 0, 'CALLS_LTP': 0, 'CALLS_Net_Chng': 0, 'CALLS_Bid_Qty': 0, 'CALLS_Bid_Price': 0,
                  'CALLS_Ask_Price': 0, 'CALLS_Ask_Qty': 0, 'Strike_Price': 0, 'PUTS_OI': 0, 'PUTS_Chng_in_OI': 0,
                  'PUTS_Volume': 0, 'PUTS_IV': 0, 'PUTS_LTP': 0, 'PUTS_Net_Chng': 0, 'PUTS_Bid_Qty': 0,
                  'PUTS_Bid_Price': 0, 'PUTS_Ask_Price': 0, 'PUTS_Ask_Qty': 0}

        # print(expiry_date)
        for m in range(len(payload['records']['data'])):
            if not expiry_date or (payload['records']['data'][m]['expiryDate'] == expiry_date):
                try:
                    oi_row['Expiry_Date'] = payload['records']['data'][m]['expiryDate']
                    oi_row['CALLS_OI'] = payload['records']['data'][m]['CE']['openInterest']
                    oi_row['CALLS_Chng_in_OI'] = payload['records']['data'][m]['CE']['changeinOpenInterest']
                    oi_row['CALLS_Volume'] = payload['records']['data'][m]['CE']['totalTradedVolume']
                    oi_row['CALLS_IV'] = payload['records']['data'][m]['CE']['impliedVolatility']
                    oi_row['CALLS_LTP'] = payload['records']['data'][m]['CE']['lastPrice']
                    oi_row['CALLS_Net_Chng'] = payload['records']['data'][m]['CE']['change']
                    if oi_mode == 'full':
                        oi_row['CALLS_Bid_Qty'] = payload['records']['data'][m]['CE']['bidQty']
                        oi_row['CALLS_Bid_Price'] = payload['records']['data'][m]['CE']['bidprice']
                        oi_row['CALLS_Ask_Price'] = payload['records']['data'][m]['CE']['askPrice']
                        oi_row['CALLS_Ask_Qty'] = payload['records']['data'][m]['CE']['askQty']
                except KeyError:
                    oi_row['CALLS_OI'], oi_row['CALLS_Chng_in_OI'], oi_row['CALLS_Volume'], oi_row['CALLS_IV'], oi_row[
                        'CALLS_LTP'], oi_row['CALLS_Net_Chng'] = 0, 0, 0, 0, 0, 0
                    if oi_mode == 'full':
                        oi_row['CALLS_Bid_Qty'], oi_row['CALLS_Bid_Price'], oi_row['CALLS_Ask_Price'], oi_row[
                            'CALLS_Ask_Qty'] = 0, 0, 0, 0
                    pass

                oi_row['Strike_Price'] = payload['records']['data'][m]['strikePrice']

                try:
                    oi_row['PUTS_OI'] = payload['records']['data'][m]['PE']['openInterest']
                    oi_row['PUTS_Chng_in_OI'] = payload['records']['data'][m]['PE']['changeinOpenInterest']
                    oi_row['PUTS_Volume'] = payload['records']['data'][m]['PE']['totalTradedVolume']
                    oi_row['PUTS_IV'] = payload['records']['data'][m]['PE']['impliedVolatility']
                    oi_row['PUTS_LTP'] = payload['records']['data'][m]['PE']['lastPrice']
                    oi_row['PUTS_Net_Chng'] = payload['records']['data'][m]['PE']['change']
                    if oi_mode == 'full':
                        oi_row['PUTS_Bid_Qty'] = payload['records']['data'][m]['PE']['bidQty']
                        oi_row['PUTS_Bid_Price'] = payload['records']['data'][m]['PE']['bidprice']
                        oi_row['PUTS_Ask_Price'] = payload['records']['data'][m]['PE']['askPrice']
                        oi_row['PUTS_Ask_Qty'] = payload['records']['data'][m]['PE']['askQty']
                except KeyError:
                    oi_row['PUTS_OI'], oi_row['PUTS_Chng_in_OI'], oi_row['PUTS_Volume'], oi_row['PUTS_IV'], oi_row[
                        'PUTS_LTP'], oi_row['PUTS_Net_Chng'] = 0, 0, 0, 0, 0, 0
                    if oi_mode == 'full':
                        oi_row['PUTS_Bid_Qty'], oi_row['PUTS_Bid_Price'], oi_row['PUTS_Ask_Price'], oi_row[
                            'PUTS_Ask_Qty'] = 0, 0, 0, 0

                # if oi_mode == 'full':
                #     oi_row['CALLS_Chart'], oi_row['PUTS_Chart'] = 0, 0
                oi_data = pd.concat([oi_data, pd.DataFrame([oi_row])], ignore_index=True)
                oi_data['Symbol'] = symbol
                oi_data['Fetch_Time'] = payload['records']['timestamp']
        return oi_data


def expiry_dates_future():
    """
    get the future and option expiry dates as per stock or index given
    :return: list of dates
    """
    payload = nse.get_nse_option_chain("TCS").json()
    return payload['records']['expiryDates']


def expiry_dates_option_index():
    """
    get the future and option expiry dates as per stock or index given
    :return: dictionary
    """
    # data_df = pd.DataFrame(columns=['index', 'expiry_date'])
    data_dict = {}
    for ind in indices_list:
        payload = nse.get_nse_option_chain(ind).json()
        data_dict.update({ind: payload['records']['expiryDates']})
    return data_dict


nse = NSE()
if __name__ == '__main__':
    df = expiry_dates_option_index()
    print(df)
