"""API unit tests"""
import datetime
import unittest

import payday
import payday.api


class APITestCase(unittest.TestCase):
    def test_bank_holidays(self):
        self.assertListEqual(
            [
                datetime.date(2022, 1, 1),
                datetime.date(2021, 12, 31),
                datetime.date(2022, 1, 17),
                datetime.date(2022, 2, 21),
                datetime.date(2022, 5, 30),
                datetime.date(2022, 6, 19),
                datetime.date(2022, 7, 4),
                datetime.date(2022, 9, 5),
                datetime.date(2022, 10, 10),
                datetime.date(2022, 11, 11),
                datetime.date(2022, 11, 24),
                datetime.date(2022, 12, 25),
                datetime.date(2022, 12, 26),
            ],
            payday.api.bank_holidays(2022),
        )

    def test_is_pay_day_month_end(self):
        self.assertTrue(payday.is_pay_day(datetime.date(2021, 3, 31)))

    def test_is_pay_day_month_end_holiday(self):
        self.assertFalse(payday.is_pay_day(datetime.date(2021, 5, 31)))

    def test_is_pay_day_month_end_holiday_adjustment(self):
        self.assertTrue(payday.is_pay_day(datetime.date(2021, 5, 28)))

    def test_is_pay_day_mid_month(self):
        self.assertTrue(payday.is_pay_day(datetime.date(2021, 1, 15)))

    def test_is_pay_day_mid_month_holiday(self):
        self.assertFalse(payday.is_pay_day(datetime.date(2021, 2, 15)))

    def test_is_pay_day_mid_month_holiday_adjustment(self):
        self.assertTrue(payday.is_pay_day(datetime.date(2021, 2, 12)))

    def test_next_pay_date_on_date(self):
        self.assertEqual(
            datetime.date(2021, 5, 14),
            payday.next_pay_day(datetime.date(2021, 5, 14)),
        )

    def test_next_pay_date_in_the_future(self):
        self.assertEqual(
            datetime.date(2021, 5, 28),
            payday.next_pay_day(datetime.date(2021, 5, 15)),
        )

    def test_pay_day_gen(self):
        gen = payday.pay_days_gen(start=datetime.date(2021, 4, 4))
        self.assertEqual(datetime.date(2021, 4, 15), next(gen))
        self.assertEqual(datetime.date(2021, 4, 30), next(gen))
        # weekend adjustment
        self.assertEqual(datetime.date(2021, 5, 14), next(gen))
        # holiday adjustment
        self.assertEqual(datetime.date(2021, 5, 28), next(gen))
