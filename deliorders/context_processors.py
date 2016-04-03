# -*- coding: utf-8 -*-

from django.utils import timezone
from deliorders.utils import *

def check_timeframe(request):
    ret = {
        'tf_next_start': None,
        'tf_next_end': None,
        'tf_closed': False,
        'tf_confirmed': False
    }

    if request.user.is_authenticated():
        now = timezone.now()

        ret['tf_closed'] = is_tf_closed(now)
        ret['tf_delivery_start'], ret['tf_delivery_end'] = delivery_days(now)

        if ret['tf_closed']:
            # Check if user already confirmed timeframe for this week
            if not hasattr(request.user, 'customer'):
                ret['tf_confirmed'] = True
                return ret
            customer = request.user.customer
            when_last_confirmed = customer.last_confirmed_tf or datetime.datetime(2015,1,1,0,0,0)

            if tf_is_after_last_window(when_last_confirmed):
                ret['tf_confirmed'] = True
    
    return ret
