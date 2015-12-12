"""Products views."""

from django.http import JsonResponse
from django.db.models import Q, Min

from deliproducts.models import Product


def search_ajax(request):
    """View that accepts a "q" GET parameter and searches products matching."""
    q = request.GET['q']
    products = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q)
    )

    ret = []
    for product in products:
        price = product.price_set.aggregate(Min('sell_price'))['sell_price__min']
        ret.append(
            {
                'id': product.id,
                'category': product.category.__str__(),
                'name': "%s ($%.2f)" % (product.__str__(), price),
                'price': price
            }
        )
    return JsonResponse(ret, safe=False)
