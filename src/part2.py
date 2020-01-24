from part1 import excel_to_dataframes
import pandas as pd
from datetime import timedelta

dataframes, xlim = excel_to_dataframes()


def find_max_profit_days(weekdays):
    # weekdays is a pandas dataframe
    min_price = 9999999999
    max_profit = 0
    buy_date = None
    sell_date = None
    buy_price = None
    sell_price = None
    for index, item in weekdays.iterrows():
        price = item['Bid Close']
        if price < min_price:
            buy_price = price
            min_price = price
            buy_date = item['Date']
        elif price - min_price > max_profit:
            sell_price = price
            max_profit = sell_price - min_price
            sell_date = item['Date']
    return (buy_date, buy_price), (sell_date, sell_price), max_profit


def calculate(sheet='Gold Spot', months=None):
    if not months:
        months = [3, 6, 9, 12]
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
    for monday, (buy, sell, profit) in data.items():
        friday = monday + timedelta(4)
        print('Maximum profit week {} to {} is {:.2f}, buy at {:.2f} on {}, sell at {:.2f} on {}'.
              format(monday.strftime('%m/%d/%Y'),
                     friday.strftime('%m/%d/%Y'),
                     profit,
                     buy[1],
                     buy[0].strftime('%m/%d/%Y'),
                     sell[1],
                     sell[0].strftime('%m/%d/%Y')
                     )
              )


def main():
    data = calculate()
    display_data(data)


if __name__ == "__main__":
    main()
