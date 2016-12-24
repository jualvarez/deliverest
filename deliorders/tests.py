from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .utils import *


class TimeFrameTestCase(TestCase):

    def test_order_narrow_closed(self):
        now = timezone.localtime(timezone.now())
        weekly_start = now.weekday()
        hour_start = now.hour
        with self.settings(
            WEEKLY_WINDOW_START=weekly_start,
            WEEKLY_WINDOW_END=weekly_start,
            WEEKLY_WINDOW_START_HOUR=hour_start,
            WEEKLY_WINDOW_END_HOUR=hour_start,
        ):
            self.assertEqual(is_tf_closed(), True)

    def test_order_narrow_open(self):
        now = timezone.localtime(timezone.now())
        weekly_start = now.weekday()
        hour_start = now.hour + 1
        with self.settings(
            WEEKLY_WINDOW_START=weekly_start,
            WEEKLY_WINDOW_END=weekly_start,
            WEEKLY_WINDOW_START_HOUR=hour_start,
            WEEKLY_WINDOW_END_HOUR=hour_start,
        ):
            self.assertEqual(is_tf_closed(), False)

    def test_next_delivery_date_when_tf_open(self):
        now = timezone.localtime(timezone.now())
        weekly_start = now.weekday()
        hour_start = now.hour + 1
        delivery_date = now + timedelta(1)
        with self.settings(
            WEEKLY_WINDOW_START=weekly_start,
            WEEKLY_WINDOW_END=weekly_start,
            WEEKLY_WINDOW_START_HOUR=hour_start,
            WEEKLY_WINDOW_END_HOUR=hour_start,
        ):
            calc_delivery = next_open_day(timezone.now(), weekly_start + 1)
            self.assertEqual(
                (calc_delivery.year, calc_delivery.month, calc_delivery.day),
                (delivery_date.year, delivery_date.month, delivery_date.day)
            )

    def test_next_delivery_date_when_tf_closed(self):
        now = timezone.localtime(timezone.now())
        weekly_start = now.weekday()
        hour_start = now.hour
        delivery_date = now + timedelta(8)
        with self.settings(
            WEEKLY_WINDOW_START=weekly_start,
            WEEKLY_WINDOW_END=weekly_start,
            WEEKLY_WINDOW_START_HOUR=hour_start,
            WEEKLY_WINDOW_END_HOUR=hour_start,
        ):
            calc_delivery = next_open_day(timezone.now(), weekly_start + 1)
            self.assertEqual(
                (calc_delivery.year, calc_delivery.month, calc_delivery.day),
                (delivery_date.year, delivery_date.month, delivery_date.day)
            )
