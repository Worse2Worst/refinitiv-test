import unittest
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, '../src/')  # change path so that it can find the modules

from part1 import excel_to_dataframes
from part2 import calculate, display_data

dataframes, xlim = excel_to_dataframes()


class TestPart1(unittest.TestCase):
    # Verify that the %Daily Returns are correct
    def test_daily_return_values(self):
        for sheet_name, data in dataframes.items():
            for index in range(0, len(data)):
                price = data['Bid Close'][index]
                daily_return = data['% Daily Return'][index]
                date = data['Date'][index].date()
                # The first day of a year has no daily return, since it has no previous day
                if date.day == 1 and date.month == 1:
                    self.assertTrue(np.isnan(daily_return), msg="The first day of the year doesn't has daily return.")
                else:
                    # Manually calculate the daily return as in the Refinitiv instructions
                    previous_day_price = data['Bid Close'][index - 1]
                    daily_return2 = ((price - previous_day_price) / previous_day_price) * 100
                    self.assertTrue(np.isclose(daily_return, daily_return2),
                                    msg='There might be some miscalculation of the daily returns.')


class TestPart2(unittest.TestCase):

    # Test the calculate maximum profits function for EVERY Sheets and EVERY months in the Excel File
    # Must buy before sell, max_profit must equals to (sell_price - buy_price)
    def test_calculate_integrity(self):
        for sheet_name, _ in dataframes.items():
            months = list(range(1, 12 + 1))
            data = calculate(sheet=sheet_name, months=months)
            for k, v in data.items():
                buy_date = v[0][0]
                buy_price = v[0][1]
                sell_date = v[1][0]
                sell_price = v[1][1]
                max_profit = v[2]
                self.assertGreaterEqual(max_profit, 0, msg='Profits should be none-negative.')
                # In case the prices go down everyday, can't make a profit at all
                if buy_date is None:
                    self.assertIsNone(sell_date)
                    self.assertEqual(max_profit, 0, msg='There is no profits for this week.')
                # We can make a profit this week
                else:
                    self.assertTrue(buy_date < sell_date, msg='Buy dates must be earlier than sell dates.')
                    self.assertTrue(np.isclose(sell_price - buy_price, max_profit),
                                    msg='There might be some miscalculation of the maximum profits.')

    # Compare some of the results to the known solutions
    def test_calculate_values(self):
        data = calculate(sheet='Palladium Spot', months=[1])
        profits = [27.0, 78.0, 40.5]
        for i, (k, v) in enumerate(data.items()):
            profit = v[2]
            self.assertAlmostEqual(profit, profits[i])

    # Print results to check that the display_data function works correctly.
    def test_display(self):
        data = calculate(sheet='Gold Spot', months=[6])
        print()
        print('################################# (Unit Test) ##############################################')
        display_data(data)
        print('############################################################################################')


if __name__ == '__main__':
    unittest.main()
