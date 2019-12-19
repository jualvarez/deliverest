# -*- coding: utf-8 -*-

from functools import wraps

from constance import config
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.text import ugettext_lazy as _


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs)
            if isinstance(out, dict):
                out = render(request, tpl, out)
            return out
        return wrapper
    return decorator


def suspendable_view(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if config.ORDERS_SUSPENDED:
            raise PermissionDenied(_(u"Las órdenes están momentaneamente suspendidas: {}").format(config.ORDERS_SUSPENDED_REASON))
        return func(request, *args, **kwargs)
    return wrapper

