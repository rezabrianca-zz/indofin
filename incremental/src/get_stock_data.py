#!/usr/bin/python3
import pandas as pd
import numpy as np
import time
import os

os.chdir('/home/ubuntu/indofin/incremental/src/')
today = pd.to_datetime('today').strftime('%Y-%m-%d')
apikey = os.getenv('API_KEY')

stock_df = pd.read_csv('../data/raw/kode_saham_{0}.csv'.format(date))[['Kode', 'Nama']]
selected = pd.read_csv('../data/preprocessed/net_profit_growth/percent_growth_{0}.csv'.format(today))

joined_df = pd.merge(stock_df, selected, left_on='Kode', right_on='stock_label')
joined_df = joined_df[['stock_label', 'Nama', 'profit_growth_mean', 'profit_growth_median']]

low_threshold = joined_df.describe()['profit_growth_median'][5]
high_threshold = joined_df.describe()['profit_growth_median'][6]

selected_df = joined_df[joined_df['profit_growth_median'] > low_threshold]

s_list = []
s_mean = []
s_median = []
last_price_list = []

print('Begin get stock adjusted price.')
for stock in selected_df.stock_label:
    try:
        dt = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={0}.JK&apikey={1}&datatype=csv'.format(stock, apikey), usecols=['timestamp', 'adjusted close'])
        dt.timestamp = pd.to_datetime(dt.timestamp)
        last_price = dt['adjusted close'][0]
        dt_sorted = dt.sort_values('timestamp').reset_index().drop('index', axis=1).copy()

        d = []
        p = []
        for i, s in dt_sorted.iterrows():
            if s.timestamp.month == 3:
                d.append(s['timestamp'])
                p.append(s['adjusted close'])
            elif s.timestamp.month == 6:
                d.append(s['timestamp'])
                p.append(s['adjusted close'])
            elif s.timestamp.month == 9:
                d.append(s['timestamp'])
                p.append(s['adjusted close'])
            elif s.timestamp.month == 12:
                d.append(s['timestamp'])
                p.append(s['adjusted close'])

        s_data = pd.DataFrame.from_dict({
                'stock_label': stock,
                'date': d,
                'adjusted_price': p
                })

        s_data = s_data[s_data.adjusted_price != 0].reset_index().drop('index', axis=1)
        gain = [None]
        for i in range(1, s_data.shape[0]):
            gain.append(100.0*(np.log(s_data.adjusted_price[i]/s_data.adjusted_price[i-1])))

        s_data['percent_gain'] = gain

        s_data = s_data.dropna()
        s_data.to_csv('../data/raw/stock_data/{0}.csv'.format(stock), index=False)

        s_change_mean = s_data.percent_gain.describe()[1]
        s_change_median = s_data.percent_gain.describe()[5]
        print(stock)
        s_list.append(stock)
        s_mean.append(s_change_mean)
        s_median.append(s_change_median)
        last_price_list.append(last_price)
        time.sleep(15)

    except Exception:
        print('Stock data not found for {0}'.format(stock))
        pass
print('Finish getting stock data.')
