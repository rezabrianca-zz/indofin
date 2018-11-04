#!/usr/bin/python3
import pandas as pd
import os

os.chdir('/home/ubuntu/indofin/incremental/src/')
source_path = '../data/raw/stock_data/'

today = pd.to_datetime('today').strftime('%Y-%m-%d')
stock_df = pd.read_csv('../data/raw/kode_saham_{0}.csv'.format(today))[['Kode', 'Nama']]
selected = pd.read_csv('../data/preprocessed/net_profit_growth/percent_growth_{0}.csv'.format(today))

joined_df = pd.merge(stock_df, selected, left_on='Kode', right_on='stock_label')
joined_df = joined_df[['stock_label', 'Nama', 'profit_growth_mean', 'profit_growth_median']]

low_threshold = joined_df.describe()['profit_growth_median'][5]

selected_df = joined_df[joined_df['profit_growth_median'] > low_threshold]

s_list = []
s_mean = []
s_median = []

print('Begin get top consideration company.')
for f in os.listdir(source_path):
    if '.csv' in f:
        s_data = pd.read_csv(source_path + f)
        s_change_mean = s_data.percent_gain.describe()[1]
        s_change_median = s_data.percent_gain.describe()[5]
        s_list.append(f.split('.')[0])
        s_mean.append(s_change_mean)
        s_median.append(s_change_median)

stock_data = pd.DataFrame.from_dict({
            'stock_label':s_list,
            'stock_growth_mean':s_mean,
            'stock_growth_median':s_median
            })

complete_df = pd.merge(selected_df, stock_data, on='stock_label')

threshold = complete_df.stock_growth_median.describe()[5]
top_consideration = complete_df[complete_df['stock_growth_median'] > threshold].copy()
top_consideration = top_consideration[['stock_label', 'Nama', 'profit_growth_mean', 'profit_growth_median', 'stock_growth_mean', 'stock_growth_median']]
top_consideration.to_csv('../data/preprocessed/top_consideration/top_consideration_{0}.csv'.format(today), index=False)
print('Top consideration at {0} successfully created.'.format(today))
