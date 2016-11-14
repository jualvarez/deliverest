# -*- coding: utf-8 -*-

from datetime import datetime

from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.utils import timezone

from deliverest.decorators import render_to
from deliproducts.models import Category, Price
from deliorders.models import Order, OrderItem
from deliorders import utils
from delicontacts.models import Customer
from delidelivery.models import DeliveryMethod
from delicontent.models import PromoImage


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@render_to('home.html')
def home(request, *args, **kwargs):
    catslug = kwargs.get('category', None)

    context = {}
    if catslug is not None:
        if catslug == settings.CATEGORY_SLUG_FOR_OTHER:
            category = None
        else:
            category = get_object_or_404(Category, slug=catslug)
        context['products'] = Price.objects.filter(Q(product__category__parent=category) | Q(product__category=category), product__is_active=True, is_active=True)
        context['category_browse'] = True
        context['selected_category'] = category
    else:
        context['products'] = Price.objects.filter(featured=True, product__is_active=True, is_active=True)
        context['promo_images'] = PromoImage.objects.filter(is_active=True)

    return context


@render_to('home.html')
def search(request, *args, **kwargs):
    # This should be the same query as deliproducts.views.search_ajax
    q = request.GET['q']
    products = Price.objects.filter(
        Q(presentation__name__icontains=q) | Q(product__name__icontains=q) | Q(product__description__icontains=q),
        is_active=True, product__is_active=True
    )

    context = {}
    context['products'] = products
    context['category_browse'] = True
    context['category_header'] = 'Búsqueda'
    context['category_header_additional'] = q

    return context


@login_required
@render_to('cart.html')
def cart(request, *args, **kwargs):
    # This should always return a customer. Let the error propagate otherwise.
    c = request.user.customer
    o = Order.objects.get_active(c)
    if o is None:
        try:
            o = Order.objects.filter(customer=c, status=20).order_by('-when_create')[0]
        except IndexError:
            o = None
    if o is not None:
        item_ids = [item.id for item in o.orderitem_set.all()]
        if request.POST:
            # Modify order
            for mod in request.POST:
                if "quantity_" not in mod and "comment_" not in mod:
                    continue
                item_id = mod.split("_")[1]
                if int(item_id) not in item_ids:
                    return HttpResponseBadRequest("Intent to change inexistent item: " + mod)
                try:
                    item = OrderItem.objects.get(id=item_id)
                except OrderItem.DoesNotExist:
                    continue
                if "quantity_" in mod:
                    val = int(request.POST[mod])
                    if val == 0:
                        item.delete()
                    elif val > 0:
                        item.quantity = val
                        item.save()
                if "comment_" in mod:
                    val = unicode(request.POST[mod])
                    item.comments = val
                    item.save()
        o.save()

    context = {
        'empty_cart': o is None or not o.orderitem_set.all().count(),
        'order': o,
        'delivery_methods': DeliveryMethod.objects.all(),
        'customer': c
    }
    return context


@login_required
def confirm_cart(request, *args, **kwargs):
    # should always be a POST from the shopping cart
    if not request.POST:
        raise Http404("Page not found")
    # This should always return a customer. Let the error propagate otherwise.
    c = request.user.customer

    # Try to get a user unconfirmed cart
    o = Order.objects.get_active(c)
    if not o:
        raise Http404("El usuario no tiene una order abierta.")
    o.contact_mode = 50  # Web
    o.status = 20  # User confirmed order
    OrderForm = modelform_factory(Order, fields=('delivery_method', 'delivery_address', 'user_comments'))
    form = OrderForm(request.POST, request.FILES, instance=o)
    if form.is_valid():
        dm = form.cleaned_data['delivery_method']
        form.instance.delivery_date = dm.next_delivery_date()
        form.save()
        # Update customer's data with latest delivery address
        c.address = form.instance.delivery_address
        c.save()
    else:
        raise Exception("Los datos ingresados son inválidos")

    return redirect('shopping_cart')


@render_to('cart_status.html')
def cart_status(request, *args, **kwargs):
    if not request.user.is_authenticated():
        return {}

    # This should always return a customer. Let the error propagate otherwise.
    c = Customer.objects.get(associated_user=request.user)
    o = Order.objects.get_active(c)

    context = {
        'order': o
    }
    return context


@render_to('add_dialog.html')
def add_dialog(request):
    is_logged_in = request.user.is_authenticated()

    o = None
    if is_logged_in:
        c = request.user.customer
        o = Order.objects.get_active(c)

    price_id = request.GET.get('product_id', None)
    price = get_object_or_404(Price, pk=price_id)
    product = price.product
    if o is not None:
        existing_items = o.orderitem_set.filter(product__product=product)
    else:
        existing_items = []
    return {
        'product': product,
        'selected_price': price,
        'existing_items': existing_items,
        'is_logged_in': is_logged_in
    }


def _add_to_cart(customer, price, quantity, comments=None):
    # Try to find an order open for this customer
    o = Order.objects.get_active(customer)
    if o is None or o.status == 20:
        o = Order()
        o.customer = customer
        o.contact_mode = 50  # Web
        o.status = 10
        o.delivery_method = customer.prefered_delivery_method
        o.delivery_address = customer.address
        o.save()

    # See if an item of the same Price was already added and add up quantities if it's the case
    try:
        # TODO: Could be a problem if the same Price was added manually through admin
        i = OrderItem.objects.get(order=o, product=price)
        i.quantity = i.quantity + float(quantity)
    except ObjectDoesNotExist:
        i = OrderItem()
        i.order = o
        i.quantity = float(quantity)
        i.product = price

    if comments:
        i.comments = comments
    i.save()

    # Check for final quantity, delete if 0 or negative
    if i.quantity <= 0:
        i.delete()
        i = None

    return i


def add_to_cart(request):
    if not request.user.is_authenticated():
        return JsonResponse({'success': False, 'error': _(u'Antes de crear un carrito de compras, tenés que acceder al sistema.')})
    price_id = request.GET.get('price_id', '')
    quantity = request.GET.get('quantity', '')
    comments = request.GET.get('comments', '')

    if price_id == '' or quantity == '':
        return JsonResponse({'success': False, 'error': _(u'¿Cuántos querés?')})

    try:
        p = Price.objects.get(id=price_id)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': _(u'¡Ups! No encontramos el producto que quisiste agregar. Lo vamos a verificar.')})

    # This should always return a customer. Let the error propagate otherwise.
    c = request.user.customer

    i = _add_to_cart(c, p, quantity, comments)
    if i is None:
        return JsonResponse({'success': True, 'message': _((u'Sacamos <strong>%s</strong> del carrito de compras') % (p.product.name))})

    return JsonResponse({'success': True, 'message': _((u'Ahora tenés %d <strong>%s</strong> en el carrito de compras') % (i.quantity, p.product.name))})


@login_required
def user_confirmed_tf(request):
    customer = request.user.customer
    customer.last_confirmed_tf = datetime.today()
    customer.save()
    return JsonResponse({'success': True})


@login_required
def load_order(request):
    order_id = request.POST.get('order_id')

    customer = request.user.customer

    history_order = Order.objects.get(id=order_id, customer=customer)

    for item in history_order.orderitem_set.all():
        _add_to_cart(customer, item.product, item.quantity)

    return redirect(urlresolvers.reverse('shopping_cart'))
