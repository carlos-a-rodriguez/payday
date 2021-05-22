"""API unit tests"""
import datetime
import unittest

import payday
import payday.api


class APITestCase(unittest.TestCase):
    def setUp(self):
        payday.api.bank_holidays.cache_clear()

    def test_bank_holidays(self):
        self.assertListEqual(
            payday.api.bank_holidays(2022),
            [
                datetime.date(2022, 1, 1),
                datetime.date(2021, 12, 31),
                datetime.date(2022, 1, 17),
                datetime.date(2022, 2, 21),
                datetime.date(2022, 5, 30),
                datetime.date(2022, 7, 4),
                datetime.date(2022, 9, 5),
                datetime.date(2022, 10, 10),
                datetime.date(2022, 11, 11),
                datetime.date(2022, 11, 24),
                datetime.date(2022, 12, 25),
                datetime.date(2022, 12, 26),
            ]
        )

    def test_bank_holidays_cache(self):
        _ = payday.api.bank_holidays(2021)  # miss
        _ = payday.api.bank_holidays(2021)  # hit
        _ = payday.api.bank_holidays(2022)  # miss

        self.assertEqual(payday.api.bank_holidays.cache_info().hits, 1)
        self.assertEqual(payday.api.bank_holidays.cache_info().misses, 2)

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

    def test_next_pay_date(self):
        self.assertEqual(
            payday.next_pay_day(datetime.date(2021, 5, 14)),
            datetime.date(2021, 5, 14),
            msg="next_pay_day should include the date specified"
        )
        self.assertEqual(
            payday.next_pay_day(datetime.date(2021, 5, 15)),
            datetime.date(2021, 5, 28),
        )

    def test_pay_day_gen(self):
        gen = payday.pay_days_gen(date=datetime.date(2021, 4, 4))
        self.assertEqual(next(gen), datetime.date(2021, 4, 15))
        self.assertEqual(next(gen), datetime.date(2021, 4, 30))
        self.assertEqual(next(gen), datetime.date(2021, 5, 14))  # weekend adjustment
        self.assertEqual(next(gen), datetime.date(2021, 5, 28))  # holiday adjustment
