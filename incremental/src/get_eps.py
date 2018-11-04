#!/usr/bin/python3
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os

from slack_message import sendMessage

os.chdir('/home/ubuntu/indofin/incremental/src/')
today = pd.to_datetime('today').strftime('%Y-%m-%d')

# setup
opts = Options()
opts.set_headless()
opts.add_argument('log-level=3') # suppress warning

assert opts.headless
browser = Chrome('/usr/bin/chromedriver', options=opts)
browser.implicitly_wait(2)

stock_list = pd.read_csv('../data/preprocessed/top_consideration/top_consideration_{0}.csv'.format(today))

sendMessage('Begin get EPS data.')
print('Begin get EPS data.')
try:
    for st in stock_list.stock_label:
        print('Open webpage for {0}'.format(st))
        # open web page
        browser.get('https://www.indopremier.com/ipotmember/newsSmartSearch.php?code={0}'.format(st))
        print('Click fundamental menu for {0}'.format(st))

        # click menu fundamental
        browser.find_element_by_partial_link_text('fundamental').click()
        print('Select annual data for {0}'.format(st))
        time.sleep(5)
        # select annual data
        select = Select(browser.find_element_by_id('quarterFundamental'))
        select.select_by_value('4')
        # select.select_by_visible_text('12 Month')
        time.sleep(1)

        print('Click GO for {0}'.format(st))
        # click GO
        browser.find_element_by_xpath("//button[@class='btn btn-default btn-xs-input']").click()
        time.sleep(5)
        print('Get all data for {0}'.format(st))
        # get all data
        all_data = browser.find_element_by_id('popInfoContent').text.split('\n')
        time.sleep(5)

        # get year list and convert as int
        year_list = [r.strip() for r in all_data[6].split('12M')][-6:]
        year_list = [int(e) for e in year_list]

        # get EPS data and convert as float
        eps_list = browser.find_element_by_xpath("//tr[18]").text.split()[-6:]
        eps_list = [f.replace(',', '') for f in eps_list]
        eps_list = [float(g) for g in eps_list]

        eps_data = pd.DataFrame.from_dict({'year':year_list, 'eps':eps_list})

        eps_data.to_csv('../data/raw/eps_data/{0}.csv'.format(st), index=False)
        print('Get EPS for {0} is completed.'.format(st))

except Exception:
    print('Could not get complete EPS for {0}'.format(st))
    pass

finally:
    # close the browser
    browser.close()
    quit()

sendMessage('Finish getting EPS data at {0}'.format(today))
print('Finish getting EPS data at {0}'.format(today))
