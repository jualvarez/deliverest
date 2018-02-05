# -*- coding: utf-8 -*-

"""Products views."""

from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

from deliverest.decorators import render_to

from deliproducts.models import Price


@render_to('deliproducts/product.html')
def price(request, id=None, slug_id=None):
    if slug_id:
        id = slug_id.split('-')[0]
    price = get_object_or_404(Price, id=id)
    if slug_id != price.slug_id:
        return redirect(price, permanent=True)
    return {
        'price': price,
        'category_browse': True
    }


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
