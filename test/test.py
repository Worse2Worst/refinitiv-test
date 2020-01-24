import unittest
import sys
import numpy as np

sys.path.insert(0, '../src/')  # change path so that it can find the modules

from part1 import excel_to_dataframes
from part2 import find_max_profit_days, calculate, display_data

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
                    self.assertTrue(np.isnan(daily_return), "The first day of the year doesn't has daily return.")
                else:
                    # Manually calculate the daily return as in the Refinitiv instructions
                    previous_day_price = data['Bid Close'][index - 1]
                    daily_return2 = ((price - previous_day_price) / previous_day_price) * 100
                    self.assertTrue(np.isclose(daily_return, daily_return2),
                                    "There might be some miscalculation of the daily returns.")


class TestPart2(unittest.TestCase):
    # Test calculate maximum profits for Silver Spot, January only
    def test_calculate_silver_spot_january(self):
        data = calculate(sheet='Silver Spot', months=[1])
        display_data(data)


if __name__ == '__main__':
    unittest.main()
