# -*- coding: utf-8 -*-

"""Support methdos for deliorders."""

import datetime
from django.utils import timezone
from constance import config


def tf_frame(ref_date=None):
    """Returns a tupple (start, end) for the timeframe"""
    if not ref_date:
        ref_date = timezone.now()

    ref_date = timezone.datetime(year=ref_date.year, month=ref_date.month, day=ref_date.day)
    ref_date = timezone.make_aware(ref_date)
    days_to_start = (config.WEEKLY_WINDOW_START - ref_date.weekday()) % 7
    start_hour = config.WEEKLY_WINDOW_START_HOUR
    td_start = datetime.timedelta(days=days_to_start, hours=start_hour)

    days_to_end = (config.WEEKLY_WINDOW_END - ref_date.weekday()) % 7
    end_hour = config.WEEKLY_WINDOW_END_HOUR
    td_end = datetime.timedelta(days=days_to_end, hours=end_hour, minutes=59)

    tf_start = ref_date + td_start
    tf_end = ref_date + td_end

    if tf_start > tf_end:
        tf_start = tf_start - datetime.timedelta(days=7)

    return tf_start, tf_end


def is_tf_closed(ref_date=None):
    """Check if order timeframe is closed for a given date."""

    if not ref_date:
        ref_date = timezone.now()

    tf_start, tf_end = tf_frame(ref_date)

    return tf_start < ref_date < tf_end


def date_is_after_last_window(tzdatetime):
    """Check if given date falls after the last window has closed."""
    now = timezone.now()
    now = timezone.datetime(year=now.year, month=now.month, day=now.day)
    now = timezone.make_aware(now)
    days_from_end = (((now.weekday() - config.WEEKLY_WINDOW_END) % 7) * -1) or -7
    end_hour = config.WEEKLY_WINDOW_END_HOUR
    td_end = datetime.timedelta(days=days_from_end, hours=end_hour)
    last_tf_end = now + td_end
    return tzdatetime >= last_tf_end


def delivery_days(date):
    """Calculate delivery timeframe."""
    tf_delivery_start = config.WEEKLY_DELIVERY_START
    tf_delivery_end = config.WEEKLY_DELIVERY_END

    start = date + datetime.timedelta((tf_delivery_start - date.weekday()) % 7)
    end = date + datetime.timedelta((tf_delivery_end - date.weekday()) % 7)
    if end < start:
        end += datetime.timedelta(days=7)

    # Move delivery dates a week ahead if delivery is currently closed
    if is_tf_closed(date):
        start += datetime.timedelta(days=7)
        end += datetime.timedelta(days=7)

    return start, end


def next_open_day(date, weekday):
    """Calculate next open order timeframe date."""
    next_weekday = date + datetime.timedelta((weekday - date.weekday()) % 7)
    if is_tf_closed(date):
        next_weekday += datetime.timedelta(days=7)

    return next_weekday
