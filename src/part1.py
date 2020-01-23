import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# Read the Excel file and return a dictionary of {'sheet_name' -> Pandas data_frame from that sheet}
# Note: The file is already sorted, but just sort it anyway to be sure
# Note2: This function also compute the values of '% Daily Return' and add to the new column
def excel_to_dataframes(file_path='files/PreciousMetalSpot.xlsx'):
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
    return dataframes, min_val, max_val


dataframes, min_val, max_val = excel_to_dataframes()
fig, axs = plt.subplots(len(dataframes), 1, sharey=True, tight_layout=True)
i = 0
for title, data in dataframes.items():
    values = dataframes[title]['% Daily Return'].dropna()
    axs[i].xaxis.set_major_formatter(mtick.PercentFormatter())
    axs[i].set_title(title)
    axs[i].hist(dataframes[title]['% Daily Return'].dropna(), bins=60)
    i += 1
