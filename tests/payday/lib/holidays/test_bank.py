import datetime
import unittest

from payday.lib.holidays.bank import USBankHolidays


class USBankHolidaysTestCase(unittest.TestCase):
    def test_us_bank_holidays(self):
        holidays = USBankHolidays()

        self.assertIn(datetime.date(2021, 1, 1), holidays)  # New Year's Day
        self.assertIn(datetime.date(2021, 1, 18), holidays)  # MLK Jr. Day
        self.assertIn(datetime.date(2021, 2, 15), holidays)  # President's Day
        self.assertIn(datetime.date(2021, 5, 31), holidays)  # Memorial Day
        self.assertIn(datetime.date(2021, 7, 4), holidays)  # Independence Day
        self.assertIn(datetime.date(2021, 9, 6), holidays)  # Labor Day
        self.assertIn(datetime.date(2021, 11, 25), holidays)  # Thanksgiving Day
        self.assertIn(datetime.date(2021, 12, 24), holidays)  # Christmas Day Observed
        self.assertIn(datetime.date(2021, 12, 25), holidays)  # Christmas Day
        self.assertIn(datetime.date(2021, 12, 31), holidays)  # New Year's Eve Observed

        self.assertListEqual(holidays.get_named("Columbus Day"), [])
        self.assertListEqual(holidays.get_named("Veterans Day"), [])
