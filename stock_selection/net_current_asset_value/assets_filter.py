import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from dateutil.relativedelta import relativedelta

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# trades_csv = 'Smooth Sky Blue Sheep_trades.csv'
trades_csv = 'Crawling Brown Parrot_trades.csv'

# read trade csv
trades = pd.read_csv(trades_csv, index_col = False)

# format date time string to datetime
trades['Time'] = pd.to_datetime(trades['Time'], format = '%Y-%m-%dT%H:%M:%SZ')

# format datetime to date only
trades['Time']= trades['Time'].dt.date

# time range to string
start_ = trades['Time'].iloc[0].strftime('%Y-%m')
end_ = trades['Time'].iloc[-1].strftime('%Y-%m')

# generate plots for all symbols
# symbols which only occured once will be included and printed
def plot_symbols(trades):
    '''
    Parameters
    ----------
    trades : pandas dataframe
        dataframe generated by QuantConnect order history.

    Returns
    -------
    None.
    
    Generates a folder whose named a period range, with trade prices graphs of all symbols in the DF
    '''
    
    # Turn interactive plotting off, will stop displaying in IDLE after savefig
    plt.ioff()  

    # create folder if not exist
    path = os.path.join('plots', start_ + ' to ' + end_)
    if not os.path.exists(path):
        os.makedirs(path)
    
    for symbol in trades['Symbol'].unique():      
        order = trades[trades['Symbol'] == symbol]
        if order.shape[0] != 1: # remove symbol occurs only once
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            order.plot(x='Time', y='Price')
            plt.gcf().autofmt_xdate()
            plt.savefig(os.path.join(path, symbol))
        else:
            print(symbol, 'only occurs once, therefore cannot generate plot')

def generate_report(trades):
    
    report = []
    
    last_date = trades['Time'].iloc[-1]
     
    def symbol_by_tenor_summary(symbol, tenor_values, tenor_units):
        
        
        not_enough_data = True
        summary_line = {
            'Symbol':symbol,
            'Last Traded Date':last_date,
            }
        
        for i in range(len(tenor_values)):
            tenor_value = tenor_values[i]
            tenor_unit = tenor_units[i]
            
            tenor_str = str(tenor_value) + tenor_unit
            
            if tenor_unit == 'M':
                tenor = last_date + relativedelta(months=-tenor_value)
            elif tenor_unit == 'Y':
                tenor = last_date + relativedelta(years=-tenor_value)
                
            hist = order[order['Time'] >= tenor]
            if hist.shape[0] > 1:
                not_enough_data = False
                
                start_pr = hist['Price'].iloc[0]
                end_pr = hist['Price'].iloc[-1]
                
                summary_line[tenor_str + ' Start Traded Date'] = hist['Time'].iloc[0]
                summary_line[tenor_str + ' Last Traded Date'] = hist['Time'].iloc[-1]
                summary_line[tenor_str + ' Start Price'] = start_pr
                summary_line[tenor_str + ' End Price'] = end_pr
                summary_line[tenor_str + ' Momentum'] = 'increase' if end_pr > start_pr else 'decrease'
                summary_line[tenor_str + ' PnL'] = str(100 * (end_pr - start_pr)/start_pr) + '%'
            
        if not_enough_data == False:
            return summary_line
    print(trades['Symbol'].unique())
    for symbol in trades['Symbol'].unique():
        order = trades[trades['Symbol'] == symbol]
        
        summary = symbol_by_tenor_summary(symbol, [3, 1], ['M', 'Y'])
        report.append(summary)
    
    report_df = pd.DataFrame(report)
    report_df.to_csv('report.csv', index=False)
    
    return report_df


# show symbol df for Debugging
def show_symbol_plot(symbol):
    order = trades[trades['Symbol'] == symbol]
    return order


# plot_symbols(trades)
# LSEA = show_symbol_plot('LSEA')
# ADS = show_symbol_plot('ADS')
report = generate_report(trades)
