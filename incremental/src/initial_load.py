#!/usr/bin/python3
import pandas as pd
import time
import os

from slack_message import sendMessage

os.chdir('/home/ubuntu/indofin/incremental/src/')
today = pd.to_datetime('today').strftime('%Y-%m-%d')

stock_df = pd.read_csv('../data/raw/kode_saham_{0}.csv'.format(today))[['Kode']]
stock_list = [s[0] for s in stock_df.values]
year_list = [2016, 2017, 2018]
quarter_list = ['TW1', 'TW2', 'TW3', 'Tahunan']

for stock in stock_list:
    stock_dt = []
    year_dt = []
    q_dt = []
    profit_dt = []
    for year in year_list:
        for quarter in quarter_list:
            if quarter == 'TW1':
                try:
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-I-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    stock_dt.append(stock)
                    year_dt.append(int(year))
                    q_dt.append(quarter)
                    profit_dt.append(float(df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]))
                    time.sleep(2)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    pass
            elif quarter == 'TW2':
                try:
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-II-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    stock_dt.append(stock)
                    year_dt.append(int(year))
                    q_dt.append(quarter)
                    profit_dt.append(float(df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]))
                    time.sleep(2)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    pass
            elif quarter == 'TW3':
                try:
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-III-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    stock_dt.append(stock)
                    year_dt.append(int(year))
                    q_dt.append(quarter)
                    profit_dt.append(float(df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]))
                    time.sleep(2)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    pass
            elif quarter == 'Tahunan':
                try:
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/Audit/{stock}/FinancialStatement-{year}-Tahunan-{stock}.xlsx'.format(stock=stock, year=str(year))
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    stock_dt.append(stock)
                    year_dt.append(int(year))
                    q_dt.append(quarter)
                    profit_dt.append(float(df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]))
                    time.sleep(2)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    pass

    raw_data = pd.DataFrame.from_dict(
                'stock_label': stock_dt,
                'year': year_dt,
                'quarter': q_dt,
                'profit': profit_dt
                )

    os.mkdir('../data/raw/{0}'.format(stock))

    raw_data.to_csv('../data/raw/{0}/{0}.csv'.format(stock), index=False)

sendMessage('Initial load finished.')
