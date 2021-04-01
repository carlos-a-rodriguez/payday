"""API unit tests"""
import datetime
import unittest

import payday.api


class APITestCase(unittest.TestCase):
    def test_is_pay_day_eom_day(self):
        self.assertTrue(
            payday.api.is_pay_day(
                datetime.date(2021, 3, 31)
            )
        )

    def test_is_pay_day_eom_holiday(self):
        self.assertFalse(
            payday.api.is_pay_day(
                datetime.date(2021, 5, 31)
            )
        )

    def test_is_pay_day_eom_holiday_adjustment(self):
        self.assertTrue(
            payday.api.is_pay_day(
                datetime.date(2021, 5, 28)
            )
        )

    def test_is_pay_day_mom_day(self):
        self.assertTrue(
            payday.api.is_pay_day(
                datetime.date(2021, 1, 15)
            )
        )

    def test_is_pay_day_mom_holiday(self):
        self.assertFalse(
            payday.api.is_pay_day(
                datetime.date(2021, 2, 15)
            )
        )

    def test_is_pay_day_mom_holiday_adjustment(self):
        self.assertTrue(
            payday.api.is_pay_day(
                datetime.date(2021, 2, 12)
            )
        )

    def test_next_pay_day(self):
        today = datetime.date(2021, 3, 1)
        self.assertEqual(
            payday.api.next_pay_day(today),
            today.replace(day=15)
        )

    def test_next_pay_day_on_pay_day(self):
        today = datetime.date(2021, 3, 15)
        self.assertEqual(
            payday.api.next_pay_day(today),
            today.replace(day=31)
        )

    def test_pay_days_leap_year_and_holiday(self):
        self.assertTupleEqual(
            payday.api.pay_days(2016, 2),
            (
                datetime.date(2016, 2, 12),  # 15th is MLK Jr. Day
                datetime.date(2016, 2, 29)
            )
        )

    def test_pay_days_non_leap_year(self):
        self.assertTupleEqual(
            payday.api.pay_days(2019, 2),
            (
                datetime.date(2019, 2, 15),
                datetime.date(2019, 2, 28)
            )
        )

    def test_previous_pay_day(self):
        today = datetime.date(2021, 4, 7)
        self.assertEqual(
            payday.api.previous_pay_day(today),
            payday.api.adjusted_eom_pay_day(year=2021, month=3)
        )

    def test_previous_pay_day_on_pay_day(self):
        today = datetime.date(2021, 3, 31)
        self.assertEqual(
            payday.api.previous_pay_day(today),
            payday.api.adjusted_mom_pay_day(year=today.year, month=today.month)
        )

    def test_unadjusted_eom_pay_day(self):
        today = datetime.date(2021, 5, 1)
        self.assertEqual(
            payday.api.unadjusted_eom_pay_day(today.year, today.month),
            today.replace(day=31)
        )

    def test_unadjusted_eom_pay_day_december(self):
        today = datetime.date(2021, 12, 1)
        self.assertEqual(
            payday.api.unadjusted_eom_pay_day(today.year, today.month),
            today.replace(day=31)
        )

    def test_unadjusted_eom_pay_day_feb_leap_year(self):
        today = datetime.date(2020, 2, 1)
        self.assertEqual(
            payday.api.unadjusted_eom_pay_day(today.year, today.month),
            today.replace(day=29)
        )

    def test_unadjusted_eom_pay_day_feb_non_leap_year(self):
        today = datetime.date(2021, 2, 1)
        self.assertEqual(
            payday.api.unadjusted_eom_pay_day(today.year, today.month),
            today.replace(day=28)
        )

    def test_unadjusted_mom_pay_day(self):
        today = datetime.date(2020, 2, 1)
        self.assertEqual(
            payday.api.unadjusted_mom_pay_day(today.year, today.month),
            today.replace(day=15)
        )