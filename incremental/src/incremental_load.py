#!/usr/bin/python3
import pandas as pd
import time
import os

from slack_message import sendMessage

os.chdir('/home/ubuntu/indofin/incremental/src/')

current_month = pd.to_datetime('today').month
year = pd.to_datetime('today').year
date = pd.to_datetime('today').strftime('%Y-%m-%d')

# read company list
stock_df = pd.read_csv('../data/raw/kode_saham_{0}.csv'.format(date))[['Kode']]
stock_list = [s[0] for s in stock_df.values]

# get existing company data
source_path = '../data/raw/financial_information/'
existing = []
for f in os.listdir(source_path):
    if '.csv' in f:
        existing.append(f.split('.')[0])

def process_response(url, existing_data, stock, year, quarter):
    '''
    Retrieve the necessary data from the URL
    based on current quarter

    Result: csv file for each stock containing net profit
    '''
    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
    print(stock, year, quarter)
    profit = df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]
    new_dt = pd.DataFrame.from_dict({
            'stock_label':[stock],
            'year':[int(year)],
            'quarter':[quarter],
            'profit':[profit]
            })
    existing_data = existing_data.append(new_dt, ignore_index=True)
    existing_data.drop_duplicates(keep='first', inplace=True)
    existing_data.to_csv('{0}{1}.csv'.format(source_path, stock), index=False)
    time.sleep(1)
    return

def incremental_load(stock_list, existing):
    '''
    Loop for each stock data
    Return: csv with additional data, or create new csv if the data is not exist
    '''
    for stock in stock_list:
        # if company data exist, append as new row
        if stock in existing:
            existing_data = pd.read_csv('{0}{1}.csv'.format(source_path, stock))
            existing_data = existing_data.drop_duplicates(keep='first')
            if current_month in [4,5,6]:
                try:
                    quarter = 'TW1'
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-I-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    process_response(url, existing_data, stock, year, quarter)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    time.sleep(1)
                    pass
            elif current_month in [7,8,9]:
                try:
                    quarter = 'TW2'
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-II-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    process_response(url, existing_data, stock, year, quarter)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    time.sleep(1)
                    pass
            elif current_month in [10,11,12]:
                try:
                    quarter = 'TW3'
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-III-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    process_response(url, existing_data, stock, year, quarter)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    time.sleep(1)
                    pass
            elif current_month in [1,2,3]:
                try:
                    quarter = 'Tahunan'
                    last_year = year - 1
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/Audit/{stock}/FinancialStatement-{year}-Tahunan-{stock}.xlsx'.format(stock=stock, year=last_year)
                    process_response(url, existing_data, stock, last_year, quarter)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(last_year)))
                    time.sleep(1)
                    pass
        # if not exist, create new file
        else:
            if current_month in [4,5,6]:
                try:
                    quarter == 'TW1'
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-I-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    profit = df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]
                    df = pd.DataFrame.from_dict({
                        'stock_label':[stock],
                        'year':[int(year)],
                        'quarter':[quarter],
                        'profit':[profit]
                        })
                    df.to_csv('{0}{1}.csv'.format(source_path, stock), index=False)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    time.sleep(1)
                    pass
            elif current_month in [7,8,9]:
                try:
                    quarter == 'TW2'
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-II-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    profit = df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]
                    df = pd.DataFrame.from_dict({
                        'stock_label':[stock],
                        'year':[int(year)],
                        'quarter':[quarter],
                        'profit':[profit]
                        })
                    df.to_csv('{0}{1}.csv'.format(source_path, stock), index=False)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    time.sleep(1)
                    pass
            elif current_month in [10,11,12]:
                try:
                    quarter == 'TW3'
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter}/{stock}/FinancialStatement-{year}-III-{stock}.xlsx'.format(stock=stock, year=str(year), quarter=quarter)
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    profit = df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]
                    df = pd.DataFrame.from_dict({
                        'stock_label':[stock],
                        'year':[int(year)],
                        'quarter':[quarter],
                        'profit':[profit]
                        })
                    df.to_csv('{0}{1}.csv'.format(source_path, stock), index=False)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(year)))
                    time.sleep(1)
                    pass
            elif current_month in [1,2,3]:
                try:
                    quarter == 'Tahunan'
                    last_year = year - 1
                    url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/Audit/{stock}/FinancialStatement-{year}-Tahunan-{stock}.xlsx'.format(stock=stock, year=str(last_year))
                    df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')
                    print(stock, year, quarter)
                    profit = df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0]
                    df = pd.DataFrame.from_dict({'stock_label':[stock], 'year':[int(year)], 'quarter':[quarter], 'profit':[profit]})
                    df.to_csv('{0}/{1}.csv'.format(source_path, stock), index=False)
                except Exception:
                    print('File not found for {0} - {1} - {2}'.format(stock, quarter, str(last_year)))
                    time.sleep(1)
                    pass
    return

incremental_load(stock_list, existing)
