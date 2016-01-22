# -*- coding: utf-8 -*-

"""Support methdos for deliorders."""

import datetime
from django.conf import settings


def is_tf_closed(date):
    """Check if order timeframe is closed for a given date."""
    tf_start = settings.WEEKLY_WINDOW_START
    tf_end = settings.WEEKLY_WINDOW_END

    if tf_start > tf_end:
        tf_window = tf_start - tf_end
    else:
        tf_window = (tf_start + 7) - tf_end

    tf_days = [d % 7 for d in range(tf_end, tf_end + tf_window)]
    return date.weekday() in tf_days


def tf_is_after_last_window(date):
    """Check if given date falls after the last window has closed."""
    tf_end = settings.WEEKLY_WINDOW_END
    weekday = date.weekday()
    delta = datetime.timedelta(days=((weekday-tf_end) % 7))
    last_frame_close = datetime.date.today() - delta
    return date >= last_frame_close


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
