import pandas as pd
import xlrd


# Read the Excel file and return a dictionary of {'sheet_name' -> Pandas data_frame from that sheet sorted by date(asc)}
def excel_to_dataframes(file_path='files/PreciousMetalSpot.xlsx'):
    dataframes = {}
    headers = ['Date', 'Bid Close']
    date_column = ['Date']
    sheet_names = xlrd.open_workbook(file_path, on_demand=True).sheet_names()
    for sheet_name in sheet_names:
        res[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name, names=headers,
                                        parse_dates=date_column).sort_values(by='Date')
    return dataframes


dataframes = excel_to_dataframes()

