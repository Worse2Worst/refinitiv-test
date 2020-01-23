import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.widgets import Slider
from sys import argv


file_path = 'files/PreciousMetalSpot.xlsx'
if len(argv) == 2:
    file_path = argv[1]


# Read the Excel file and return a dictionary of {'sheet_name' -> Pandas data_frame from that sheet}
# Note: The file is already sorted, but just sort it anyway to be sure
# Note2: This function also compute the values of '% Daily Return' and add to the new column
def excel_to_dataframes(file_path=file_path):
    dataframes = {}
    headers = ['Date', 'Bid Close']
    date_column = ['Date']
    min_val = 99999999
    max_val = -99999999
    sheet_names = xlrd.open_workbook(file_path, on_demand=True).sheet_names()
    for sheet_name in sheet_names:
        dataframes[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name, names=headers,
                                               parse_dates=date_column).sort_values(by='Date', ascending=False)
        dataframes[sheet_name]['% Daily Return'] = dataframes[sheet_name]['Bid Close'].pct_change(-1) * 100
        if min(dataframes[sheet_name]['% Daily Return']) < min_val:
            min_val = min(dataframes[sheet_name]['% Daily Return'])
        if max(dataframes[sheet_name]['% Daily Return']) > max_val:
            max_val = max(dataframes[sheet_name]['% Daily Return'])
    return dataframes, (min_val - 0.1, max_val + 0.1)


dataframes, xlim = excel_to_dataframes()
fig, axs = plt.subplots(len(dataframes), 1, sharey=True, tight_layout=True)
bin_size = 70
i = 0
for sheet_name, data in dataframes.items():
    values = dataframes[sheet_name]['% Daily Return'].dropna()
    axs[i].xaxis.set_major_formatter(mtick.PercentFormatter())
    axs[i].set(xlim=xlim)
    axs[i].set_title(label=sheet_name.split(' ')[0])
    axs[i].xaxis.set_major_locator(MultipleLocator((xlim[1] - xlim[0]) / bin_size))
    axs[i].yaxis.set_major_locator(MultipleLocator(5))
    axs[i].xaxis.set_minor_locator(AutoMinorLocator())
    axs[i].yaxis.set_minor_locator(AutoMinorLocator())
    axs[i].tick_params(labelrotation=90)
    axs[i].hist(dataframes[sheet_name]['% Daily Return'].dropna(), bins=bin_size)
    i += 1

plt.show()
