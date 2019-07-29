# -*- coding: utf-8 -*-

from functools import wraps

from django.template import RequestContext
from django.shortcuts import render


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
