#!/usr/bin/python3
import os
import pandas as pd
import numpy as np

from slack_message import sendMessage

os.chdir('/home/ubuntu/indofin/incremental/src/')
source_path = '../data/raw/financial_information/'
dest_path = '../data/preprocessed/financial_information/'
today = pd.to_datetime('today').strftime('%Y-%m-%d')

def quarter_profit(source_path, dest_path):
    print('Calculating Quarterly Profit ...')
    for f in os.listdir(source_path):
        if '.csv' in f:
            # read file
            s = pd.read_csv(source_path + f)
            if s.shape[0] >= 8: # only read if company has submit report based on the threshold
                # print('Stock Label \t:', f.split('.')[0])
                # print('Last Report Submitted:', s.tail(1)[['quarter', 'year']])
                profit = []
                for i in range(len(s)):
                    # depend on which quarter report company submit, will append accordingly
                    if s.quarter[i] == 'TW1':
                        profit.append(s.profit[i])
                    elif s.quarter[i] == 'TW2' and i-1 >= 0:
                        if s.quarter[i-1] == 'TW1':
                            q2p = s.profit[i] - s.profit[i-1]
                            profit.append(q2p)
                        else:
                            profit.append(None)
                    elif s.quarter[i] == 'TW3' and i-1 >= 0:
                        if s.quarter[i-1] == 'TW2':
                            q3p = s.profit[i] - s.profit[i-1]
                            profit.append(q3p)
                        else:
                            profit.append(None)
                    elif s.quarter[i] == 'Tahunan' and i-1 >= 0:
                        if s.quarter[i-1] == 'TW3':
                            q4p = s.profit[i] - s.profit[i-1]
                            profit.append(q4p)
                        else:
                            profit.append(None)
                    else:
                        profit.append(None)

                s['q_profit'] = profit
                s['percent_change'] = s.q_profit.pct_change() * 100.0
                s.to_csv(dest_path + '{0}'.format(f), index=False)
    print('Finished calculating quarterly profit.')
    return

def percent_growth(dest_path):
    print('Calculate growth per quarter ...')
    df = pd.DataFrame()
    for f in os.listdir(dest_path):
        if '.csv' in f:
            # print(f.split('.')[0])
            # read file
            s = pd.read_csv(dest_path + f)
            avg_med = s.groupby('stock_label').agg({'percent_change':['mean', 'median']}).reset_index()
            avg_med.columns = avg_med.columns.map(''.join)

            if df.empty:
                df = df.append(avg_med, ignore_index=True)
            else:
                df = pd.concat([df, avg_med], ignore_index=True)

    selected = df[(df.percent_changemean > 0) & (df.percent_changemedian > 0)]
    selected.columns = ['stock_label', 'profit_growth_mean', 'profit_growth_median']
    selected.to_csv('../data/preprocessed/net_profit_growth/percent_growth_{0}.csv'.format(today), index=False)
    print('Finish calculating net profit growth.')
    sendMessage('Finish calculating net profit growth.')
    return

quarter_profit(source_path, dest_path)
percent_growth(dest_path)
