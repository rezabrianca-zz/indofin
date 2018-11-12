#!/usr/bin/python3
import os
import pandas as pd
import numpy as np

from slack_message import sendMessage

os.chdir('/home/ubuntu/indofin/src/')
source_path = '../data/raw/financial_information/'
dest_path = '../data/preprocessed/financial_information/'
today = pd.to_datetime('today').strftime('%Y-%m-%d')

def quarter_profit(source_path, dest_path):
    print('Calculating Quarterly Profit ...')
    for f in os.listdir(source_path):
        if '.csv' in f:
            # read file
            s = pd.read_csv(source_path + f)
            if s.shape[0] >= 8 and s.profit.all() > 0: # only read if company has submit report for at least 2 years and always profitable
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
                percent_change = [None]
                for j in range(1, s.shape[0]):
                    pct_change = 100.0 * ((s.q_profit[j] - s.q_profit[j-1]) / abs(s.q_profit[j-1]))
                    percent_change.append(pct_change)
                s['percent_change'] = percent_change
                s.to_csv(dest_path + f, index=False)
    print('Finished calculating quarterly profit.')
    return

def percent_growth(dest_path):
    print('Calculate growth per quarter ...')
    sendMessage('Begin calculating net profit growth at {0}'.format(today))
    df = pd.DataFrame()
    for f in os.listdir(dest_path):
        if '.csv' in f:
            # read file
            s = pd.read_csv(dest_path + f)
            avg_med = s.groupby('stock_label').agg({'percent_change':['mean', 'median']}).reset_index()
            avg_med.columns = avg_med.columns.map(''.join)
            avg_med['last_report'] = s.tail(1)['quarter'].values[0]

            if df.empty:
                df = df.append(avg_med, ignore_index=True)
            else:
                df = pd.concat([df, avg_med], ignore_index=True)

    selected = df[(df.percent_changemean > 0) & (df.percent_changemedian > 0)]
    selected.columns = ['stock_label', 'profit_growth_mean', 'profit_growth_median', 'last_report']
    selected.to_csv('../data/preprocessed/net_profit_growth/percent_growth_{0}.csv'.format(today), index=False)
    print('Finish calculating net profit growth.')
    sendMessage('Finish calculating net profit growth at {0}.'.format(today))
    return

quarter_profit(source_path, dest_path)
percent_growth(dest_path)
