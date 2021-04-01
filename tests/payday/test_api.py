"""API unit tests"""
import datetime
import unittest

import payday


class APITestCase(unittest.TestCase):
    def test_is_pay_day_eom_day(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 3, 31)
            )
        )

    def test_is_pay_day_eom_holiday(self):
        self.assertFalse(
            payday.is_pay_day(
                datetime.date(2021, 5, 31)
            )
        )

    def test_is_pay_day_eom_holiday_adjustment(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 5, 28)
            )
        )

    def test_is_pay_day_mom_day(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 1, 15)
            )
        )

    def test_is_pay_day_mom_holiday(self):
        self.assertFalse(
            payday.is_pay_day(
                datetime.date(2021, 2, 15)
            )
        )

    def test_is_pay_day_mom_holiday_adjustment(self):
        self.assertTrue(
            payday.is_pay_day(
                datetime.date(2021, 2, 12)
            )
        )

    def test_next_pay_day(self):
        today = datetime.date(2021, 3, 1)
        self.assertEqual(
            payday.next_pay_day(today),
            today.replace(day=15)
        )

    def test_next_pay_day_on_pay_day(self):
        today = datetime.date(2021, 3, 15)
        self.assertEqual(
            payday.next_pay_day(today),
            today.replace(day=31)
        )

    def test_pay_day_iter_forward(self):
        pay_days = list(
            payday.pay_day_iter(
                datetime.date(2021, 4, 15),
                days=3,
                reverse=False,
            )
        )

        self.assertListEqual(
            pay_days,
            [
                datetime.date(2021, 4, 30),
                datetime.date(2021, 5, 14),
                datetime.date(2021, 5, 28),
            ]
        )

    def test_pay_day_iter_reverse(self):
        pay_days = list(
            payday.pay_day_iter(
                datetime.date(2021, 3, 10),
                days=3,
                reverse=True,
            )
        )

        self.assertListEqual(
            pay_days,
            [
                datetime.date(2021, 2, 26),
                datetime.date(2021, 2, 12),
                datetime.date(2021, 1, 29),
            ]
        )

    def test_pay_days_leap_year_and_holiday(self):
        self.assertTupleEqual(
            payday.pay_days(2016, 2),
            (
                datetime.date(2016, 2, 12),  # 15th is MLK Jr. Day
                datetime.date(2016, 2, 29)
            )
        )

    def test_pay_days_non_leap_year(self):
        self.assertTupleEqual(
            payday.pay_days(2019, 2),
            (
                datetime.date(2019, 2, 15),
                datetime.date(2019, 2, 28)
            )
        )

    def test_previous_pay_day(self):
        today = datetime.date(2021, 4, 7)
        self.assertEqual(
            payday.previous_pay_day(today),
            today.replace(month=3, day=31)
        )

    def test_previous_pay_day_on_pay_day(self):
        today = datetime.date(2021, 3, 31)
        self.assertEqual(
            payday.previous_pay_day(today),
            today.replace(month=3, day=15)
        )
