## Introduction
Script to get financial information from Indonesian publicly listed companies. These will run on Ubuntu 16.04 . The steps are defined as follows:
1. Get listed companies from [IDX](http://www.idx.co.id/perusahaan-tercatat/profil-perusahaan-tercatat/)
2. Get net profit from submitted financial information for [each quarter](http://www.idx.co.id/perusahaan-tercatat/laporan-keuangan-dan-tahunan/)
3. Calculate net profit per quarter
4. Calculate net profit percentage change
5. Select companies with median percentage change higher than median change from all companies
6. Get monthly adjusted close price from selected companies from stock price [provider](https://www.alphavantage.co/) - need to register for Free API Key
7. Select adjusted close price for March, June, September and December for consistency with financial performance
8. Repeat step 4 and 5 for quarterly stock performance
9. Join result from point 5 and point 8 to get companies who performs well in both financial performance and stock performance
10. Get annual EPS (earning per share) data from IndoPremier for companies selected in point 9
11. Calculate average EPS from last 6 years
12. Maximum price for the stock needs to be cheaper than:
25 times of average EPS
20 times of latest EPS
13. Upload the file result to [Slack](https://slack.com/)

Please note that IDX only keeps the data since 2016 so the financial performance evaluation will be based on performance starting from that year.

## Setup
If we install fresh Ubuntu 16.04, based on this [answer](https://askubuntu.com/questions/196768/how-to-install-updates-via-command-line), we need to update the existing packages first by running this script:
```sh
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get dist-upgrade
```
This will ensure we have the latest stable package in our environment.

### Selenium
This component is required to perform automated task in the browser. We need this since our source is not available in static page, meaning we need to click some links to get all data we need. For more details about this powerful tool, you can visit the [documentation](https://seleniumhq.github.io/selenium/docs/api/py/index.html).
To run the package smoothly, we need three components:
1. A browser installed in our Ubuntu
Since I am using Google Chrome (or Chromium in Ubuntu), I need to install it first. I followed the [tutorial](https://askubuntu.com/questions/510056/how-to-install-google-chrome) and we will have it in our environment
2. A browser driver
Since we want to perform tasks automatically, we need to use another tool to act as if the browser was opened and clicked by human. This tool will bridge the python code interaction with the browser. The setup for this was done by following commands based on this [tutorial](https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5#file-install-sh). And from selenium documentation, it expects the driver to be inside `/usr/bin/` or `/usr/local/bin/` so we also need to move the file to that folder. In addition, we need to grant the OS to execute this file. The full steps are as follows:
```sh
$ wget https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ chmod +x chromedriver
$ sudo mv -f ~/chromedriver /usr/bin/chromedriver
$ rm chromedriver_linux64.zip
```
3. Python Selenium package
Last package we need is the python selenium package itself to connect with the driver. To install this package, we can just run it using `pip`
```sh
pip install -U selenium
```
### Slack
Go to their [website](https://slack.com/) and register with your email and create organization. Don't worry, it will keep the last 10,000 messages for free and we don't need that much. We are still using Legacy Tokens to generate our token in [this](https://api.slack.com/custom-integrations/legacy-tokens) page. You need to modify line 11 and 24 or even as additional parameter in the `slack_message.py` file since I set the parameters for personal use only.

### Alpha Vantage
Go to this [link](https://www.alphavantage.co/support/#api-key) and fill the necessary fields and you will get your API token for free. Please note the free API has [limitation](https://www.alphavantage.co/premium/) to only 5 requests per minute and 500 API calls per day. If you want a bigger bandwidth, you can pay starting from $ 19.99 per month for 15 requests per minute and no daily API calls limit.

### Environment Variables
Since the scripts will run using `cronjob`, it is better to store the credentials as part of environment variables and not include as configuration file. Based on the answer [here](https://askubuntu.com/questions/58814/how-do-i-add-environment-variables), in ubuntu 16.04 we can go to the terminal and type the following:
```sh
$ sudo -H vim /etc/environment
```
We need to store two credentials namely `SLACK_TOKEN` and `API_TOKEN`. The `API_TOKEN` is the one we got from stock provider. To save these credentials, please type the following:
```
SLACK_TOKEN="YOUR_SLACK_TOKEN"
API_TOKEN="YOUR_API_TOKEN"
```
After typing, press `Esc` then followed by typing `:wq` to save the file. We need to logout and login again to our OS to make the changes permanent.

## Initial Load
There are two major parts for initial load. The first one is getting the list of public companies and then run the initial load code. To run the code, do the following:
```sh
cd ~/indofin/src/
python3 get_company.py
python3 initial_load.py
```
Since there are 600+ companies and we want to retrieve all net profit data from 2016, it means we will retrieve 10 or 11 reports for each company. I put a `time.sleep(1)` as part of the `for` loop as best practice so we will not overload the server with rapid requests. This task will run about 2 hours in total and it's better to have it run on small server rather than your own local laptop since network connection may disrupt the process. I use the smallest version of [AWS Lightsail](https://aws.amazon.com/lightsail/?nc2=h_m1) to run this code.

After the process is finished, we need to run the other files to fill our initial data. The order are as follows:
1. `net_profit_growth.py`
2. `get_stock_data.py`
3. `top_consideration.py`
4. `get_eps.py`
5. `stock_price_helper.py`

At the end of this process, we will have our first result of the companies with relatively good net profit growth and stock growth per quarter. Check out your slack message to view the result!

## Incremental Load
Now that we have the initial load ready, we can do the incremental load on daily basis. The only change we need to switch is between `initial_load.py` with `incremental_load.py`. So the final order of the work will be as follows:
1. `get_company.py`
2. `incremental_load.py`
3. `net_profit_growth.py`
4. `get_stock_data.py`
5. `top_consideration.py`
6. `get_eps.py`
7. `stock_price_helper.py`

To setup a cronjob scheduler, we need to type `crontab -e` in the terminal and follows the cron convention. We can check this [reference](https://crontab-generator.org/) to help us decide the task script. For example, I run `get_company.py` script every Monday to Friday on 00.00 UTC, so the cron task will look like this:
```sh
0 0 * * 1-5 cd ~/indofin/src/ && python3 get_company.py > /tmp/get_company.log 2>&1
```

# Closing
These scripts are for personal use only and not for commercial use. If you have some questions, feel free to reach me on my email.
