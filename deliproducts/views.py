# -*- coding: utf-8 -*-

"""Products views."""

from django.http import JsonResponse
from django.db.models import Q, Min

from deliproducts.models import Price


def search_ajax(request):
    """View that accepts a "q" GET parameter and searches products matching."""
    q = request.GET['q']
    products = Price.objects.filter(
        Q(presentation__name__icontains=q) | Q(product__name__icontains=q) | Q(product__description__icontains=q),
        is_active=True, product__is_active=True
    )

    ret = []
    for product in products:
        price = product.sell_price
        pres = product.presentation
        if not price:
            continue
        ret.append(
            {
                'id': product.id,
                'category': unicode(product.product.category),
                'name': unicode(product),
                'price': price
            }
        )
    return JsonResponse(ret, safe=False)
