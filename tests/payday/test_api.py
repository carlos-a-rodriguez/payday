"""API unit tests"""
import datetime
import unittest

import payday


class APITestCase(unittest.TestCase):
    def test_is_pay_day_month_end(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 3, 31)
            )
        )

    def test_is_pay_day_month_end_holiday(self):
        self.assertFalse(
            payday.is_pay_day(
                datetime.date(2021, 5, 31)
            )
        )

    def test_is_pay_day_month_end_holiday_adjustment(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 5, 28)
            )
        )

    def test_is_pay_day_mid_month(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 1, 15)
            )
        )

    def test_is_pay_day_mid_month_holiday(self):
        self.assertFalse(
            payday.is_pay_day(
                datetime.date(2021, 2, 15)
            )
        )

    def test_is_pay_day_mid_month_holiday_adjustment(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 2, 12)
            )
        )

    def test_pay_day_gen(self):
        gen = payday.pay_days_gen(start=datetime.date(2021, 4, 4))
        self.assertEqual(next(gen), datetime.date(2021, 4, 15))
        self.assertEqual(next(gen), datetime.date(2021, 4, 30))
        self.assertEqual(next(gen), datetime.date(2021, 5, 14))  # weekend adjustment
        self.assertEqual(next(gen), datetime.date(2021, 5, 28))  # holiday adjustment
