from part1 import excel_to_dataframes
import pandas as pd
from datetime import timedelta
import argparse

dataframes, xlim = excel_to_dataframes()
months = [3, 6, 9, 12]
sheet = 'Gold Spot'
parser = argparse.ArgumentParser(description='Part2 of the Refinitiv test.')
parser.add_argument('sheet', const=sheet, action='store_const',
                    default='Gold Spot', help='A name of sheet that we care')
parser.add_argument('months', const=months, action='store_const',
                    default=[3, 6, 9, 12], help='A list of months that we care')
args = parser.parse_args()


def find_max_profit_days(weekdays):
    # weekdays is a pandas dataframe
    min_price = 9999999999
    max_profit = 0
    buy_date = None
    sell_date = None
    for index, item in weekdays.iterrows():
        price = item['Bid Close']
        if price < min_price:
            buy_date = item['Date']
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
            sell_date = item['Date']
    return (buy_date, sell_date), max_profit


def calculate(sheet=sheet, months=months):
    df = dataframes[sheet]
    groups = df.groupby(pd.Grouper(key='Date', freq='W'))
    data = {}
    for dt, group in groups:
        monday = dt.date() - timedelta(6)
        friday = dt.date() - timedelta(2)
        if len(group) == 5 and monday.month in months and monday.month == friday.month:
            data[monday] = find_max_profit_days(group)
    return data


def display_data(data):
    return


def main():
    data = calculate()
    display_data(data)


if __name__ == "__main__":
    main()
