import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# trades_csv = 'Smooth Sky Blue Sheep_trades.csv'
trades_csv = 'Logical Magenta Scorpion_trades.csv'

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
def plot_symbols():
    # Turn interactive plotting off, will stop displaying in IDLE after savefig
    plt.ioff()  

    # create folder if not exist
    path = os.path.join('plots', start_ + ' to ' + end_)
    if not os.path.exists(path):
        os.makedirs(path)
    
    for symbol in trades['Symbol'].unique():
        print('Processing symbol:', symbol)
        order = trades[trades['Symbol'] == symbol]
        if order.shape[0] != 1: # remove symbol occurs only once
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            order.plot(x='Time', y='Price')
            plt.gcf().autofmt_xdate()
            plt.savefig(os.path.join(path, symbol))
        else:
            print(symbol, 'only occurs once, therefore cannot generate plot')

plot_symbols()

# show symbol df for Debugging
def show_symbol_plot(symbol):
    order = trades[trades['Symbol'] == symbol]
    return order

LSEA = show_symbol_plot('LSEA')
