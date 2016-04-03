# -*- coding: utf-8 -*-

"""Support methdos for deliorders."""

import datetime
from django.conf import settings
from django.utils import timezone


def is_tf_closed(date):
    """Check if order timeframe is closed for a given date."""
    now = timezone.now()
    now = timezone.datetime(year=now.year, month=now.month, day=now.day)
    now = timezone.make_aware(now)
    days_to_start = (settings.WEEKLY_WINDOW_START - now.weekday()) % 7
    start_hour = settings.WEEKLY_WINDOW_START_HOUR
    td_start = datetime.timedelta(days=days_to_start, hours=start_hour)

    days_to_end = (settings.WEEKLY_WINDOW_END - now.weekday()) % 7
    end_hour = settings.WEEKLY_WINDOW_END_HOUR
    td_end = datetime.timedelta(days=days_to_end, hours=end_hour)

    tf_start = now + td_start
    tf_end = now + td_end

    if tf_start < tf_end:
        tf_end = tf_end + datetime.timedelta(days=7)

    now = timezone.now()
    return now > tf_start and now < tf_end


def tf_is_after_last_window(tzdatetime):
    """Check if given date falls after the last window has closed."""
    now = timezone.now()
    now = timezone.datetime(year=now.year, month=now.month, day=now.day)
    now = timezone.make_aware(now)
    days_from_end = (now.weekday() - settings.WEEKLY_WINDOW_END) % 7
    end_hour = settings.WEEKLY_WINDOW_END_HOUR
    td_end = datetime.timedelta(days=days_from_end, hours=end_hour)
    last_tf_end = now - td_end
    return tzdatetime >= last_tf_end


def delivery_days(date):
    """Calculate delivery timeframe."""
    tf_delivery_start = settings.WEEKLY_DELIVERY_START
    tf_delivery_end = settings.WEEKLY_DELIVERY_END

    start = date + datetime.timedelta((tf_delivery_start-date.weekday()) % 7)
    end = date + datetime.timedelta((tf_delivery_end-date.weekday()) % 7)
    if end < start:
        end += datetime.timedelta(days=7)

    # Move delivery dates a week ahead if delivery is currently closed
    if is_tf_closed(date):
        start += datetime.timedelta(days=7)
        end += datetime.timedelta(days=7)

    return start, end


def next_open_day(date, weekday):
    """Calculate next open order timeframe date."""
    next_weekday = date + datetime.timedelta((weekday-date.weekday()) % 7)
    next_delivery_start, next_delivery_end = delivery_days(date)
    if next_weekday < next_delivery_start:
        next_weekday += datetime.timedelta(days=7)

    return next_weekday
