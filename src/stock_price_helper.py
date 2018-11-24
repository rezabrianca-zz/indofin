#!/usr/bin/python3
import pandas as pd
import numpy as np
import os

import slack_message as sm

os.chdir('/home/ubuntu/indofin/src/')
today = pd.to_datetime('today').strftime('%Y-%m-%d')
eps_path = '../data/raw/eps_data/'
growth_path = '../data/preprocessed/financial_information/'

top_df = pd.read_csv('../data/preprocessed/top_consideration/top_consideration_{0}.csv'.format(today))

stock = []
avg_eps = []
last_eps = []
for f in os.listdir(eps_path):
    if '.csv' in f:
        stock.append(f.split('.')[0])
        eps_df = pd.read_csv(eps_path + f)
        avg_eps.append(eps_df.eps.mean())
        last_eps.append(eps_df.eps[0])

eps_data = pd.DataFrame.from_dict({
            'stock':stock,
            'last_6_avg_eps':avg_eps,
            'last_eps':last_eps
            })

eps_data['avg_eps_25'] = 25 * eps_data.last_6_avg_eps
eps_data['last_eps_20'] = 20 * eps_data.last_eps

merged_data = pd.merge(top_df, eps_data, left_on='stock_label', right_on='stock', how='left')
merged_data.drop(['stock'], axis=1, inplace=True)
merged_data['diff_percent_with_avg_eps'] = round(100.0 * ((merged_data.last_price - merged_data.avg_eps_25) / merged_data.last_price), 2)
merged_data['diff_percent_with_last_eps'] = round(100.0 * ((merged_data.last_price - merged_data.last_eps_20) / merged_data.last_price), 2)

selected_data = merged_data[(merged_data.diff_percent_with_avg_eps < 0.0) & (merged_data.diff_percent_with_last_eps < 0.0) & (merged_data.last_pct_change > tol)].copy()

selected_data.to_csv('../data/output/final_data_{0}.csv'.format(today), index=False)

sm.sendMessage('Uploading output file')
sm.uploadFile('../data/output/final_data_{0}.csv'.format(today), 'Output File')
