# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:55:30 2024

@author: kenken
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
# https://pypi.org/project/yfinance/
import datetime
from dateutil.relativedelta import relativedelta

# set working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# read watchlist
watchlist = []
watchlist_name = "watchlist.txt"
with open(watchlist_name) as file:
    for line in file:
        watchlist += [line.rstrip()]
file.close()

# get dates to be used
today = datetime.datetime.now()
today_str = today.strftime('%Y-%m-%d')

one_month_prior =  (today - relativedelta(months=1)).strftime('%Y-%m-%d')
three_months_prior = (today - relativedelta(months=3)).strftime('%Y-%m-%d')
six_months_prior = (today - relativedelta(months=6)).strftime('%Y-%m-%d')
one_year_prior = (today - relativedelta(months=12)).strftime('%Y-%m-%d')

# precision format
precision = "{:.2f}"

# convert to yf compactible string
tickers_str = ''
for ticker in watchlist:
    tickers_str += ' ' + ticker
tickers_str = tickers_str[1:]

# get data from yfinance
hist = yf.download(tickers_str, period="1y")
hist.index = hist.index.strftime('%Y-%m-%d')

# process tickers
def from_hist(hist, time_start, ticker, field):
    '''

    Parameters
    ----------
    hist : pandas.DataFrame()
        history data frame.
    time_range : string
        datetime format, YYYY-MM-DD.
    ticker : string
        ticker.
    field : string
        field of data.

    Returns
    -------
    pandas.DataFrame().

    '''
    df = hist.loc[time_start:, field][ticker]
    
    new_time_start = time_start
    while df.isnull()[0]:
        new_time_start = (datetime.datetime.strptime(new_time_start, '%Y-%m-%d') + relativedelta(days=1)).strftime('%Y-%m-%d')
        df = hist.loc[new_time_start:, field][ticker]
        
    return df

# generate csv and plot results
def generate_results_plots_csv(hist, watchlist):
    columns = ['1m return', '3m return', '6m return', '1y return']
    results = pd.DataFrame(index = watchlist, columns = columns)
    
    for ticker in watchlist:
        # csv report
        one_month_series = from_hist(hist, one_month_prior, ticker, 'Close').dropna()
        three_months_series = from_hist(hist, three_months_prior, ticker, 'Close').dropna()
        six_months_series = from_hist(hist, six_months_prior, ticker, 'Close').dropna()
        one_year_series = from_hist(hist, one_year_prior, ticker, 'Close').dropna()
        
        results.loc[ticker, '1m return'] = precision.format((one_month_series[-1] - one_month_series[0])/one_month_series[0] * 100)
        results.loc[ticker, '3m return'] = precision.format((three_months_series[-1] - three_months_series[0])/three_months_series[0] * 100)
        results.loc[ticker, '6m return'] = precision.format((six_months_series[-1] - six_months_series[0])/six_months_series[0] * 100)
        results.loc[ticker, '1y return'] = precision.format((one_year_series[-1] - one_year_series[0])/one_year_series[0] * 100)
        
        # plot 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        one_year_series.plot(x='Time', y='Price')
        plt.gca().yaxis.set(ticks=np.arange(one_year_series.min(), one_year_series.max(), (one_year_series.max()-one_year_series.min())/20))
        plt.gcf().set_size_inches(30, 15)
        plt.grid()
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join('plots', ticker))
        plt.show()
        
    results.to_csv(os.path.join('results', 'results_'+today_str+'.csv'))

 
# execution       
generate_results_plots_csv(hist, watchlist)

