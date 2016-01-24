# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory

from deliverest.decorators import render_to
from deliproducts.models import Category, Product, Price
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
    context['categories'] = Category.objects.filter(is_active=True)
    if catslug is not None:
        if catslug == settings.CATEGORY_SLUG_FOR_OTHER:
            category = None
        else:
            category = get_object_or_404(Category, slug=catslug)
        context['products'] = Product.objects.filter(category=category, is_active=True)
        context['category_browse'] = True
    else:
        context['products'] = Product.objects.filter(featured=True, is_active=True)
        context['promo_images'] = PromoImage.objects.filter(is_active=True)

    return context

@login_required
@render_to('cart.html')
def cart(request, *args, **kwargs):
    # This should always return a customer. Let the error propagate otherwise.
    c = request.user.customer
    o = Order.objects.get_active(c)
    if o is not None:
        item_ids = [item.id for item in o.orderitem_set.all()]
        if request.POST:
            # Modify order
            for mod in request.POST:
                if "modify_" not in mod:
                    continue
                item_id = mod.split("_")[1]
                if int(item_id) not in item_ids:
                    return HttpResponseBadRequest("Intent to change inexistent item: "+mod)
                item = OrderItem.objects.get(id=item_id)
                val = int(request.POST[mod])
                if val == 0:
                    item.delete()
                elif val > 0:
                    item.quantity = val
                    item.save()

    context = {
        'empty_cart': o is None or not o.orderitem_set.all().count,
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

    # See if user is trying to open the cart again
    if request.POST.get('modify_order', '0') == '1':
        o = get_object_or_404(Order, customer=c, status=20)
        o.status = 10
        o.save()
        return redirect('shopping_cart')

    # Try to get a user unconfirmed cart
    o = get_object_or_404(Order, customer=c, status=10)
    o.contact_mode = 50 # Web
    o.delivery_date = utils.next_open_day(datetime.today(), o.delivery_method.delivery_day)
    o.status = 20 # User confirmed order
    OrderForm = modelform_factory(Order, fields=('delivery_method', 'delivery_address', 'comments'))
    form = OrderForm(request.POST, request.FILES, instance=o)
    if form.is_valid():
        form.save()
        # Update customer's data with latest delivery address
        c.address = form.instance.delivery_address
        c.save()
    else:
        raise Exception("dbg")

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

    product_id = request.GET.get('product_id', None)
    product = get_object_or_404(Product, pk=product_id)
    if o is not None:
        existing_items = o.orderitem_set.filter(product__product=product)
    else:
        existing_items = []
    return {
        'product': product,
        'existing_items': existing_items,
        'is_logged_in': is_logged_in
    }

def add_to_cart(request):
    if not request.user.is_authenticated():
        return JsonResponse({'success': False, 'error': _(u'Antes de crear un carrito de compras, tenés que acceder al sistema.')})
    price_id = request.GET.get('price_id', '')
    quantity = request.GET.get('quantity', '')
    if price_id == '' or quantity == '':
        return JsonResponse({'success': False, 'error': _(u'¿Cuántos querés?')})

    try:
        p = Price.objects.get(id=price_id)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': _(u'¡Ups! No encontramos el producto que quisiste agregar. Lo vamos a verificar.')})

    # This should always return a customer. Let the error propagate otherwise.
    c = Customer.objects.get(associated_user = request.user)

    # Try to find an order open for this customer
    try:
        o = Order.objects.get(customer=c, status__in=[10, 20])
        if o.status == 20:
            return JsonResponse({'success': False, 'error': _(u'Tu último pedido todavía no fue procesado. Podés modificarlo entrando al <a href="%s">carrito de compras</a>.') % urlresolvers.reverse('shopping_cart') })
    except ObjectDoesNotExist:
        o = Order()
        o.customer = c
        o.contact_mode = 50 # Web
        o.status = 10
        o.delivery_method = c.prefered_delivery_method
        o.delivery_address = c.address
        o.save()

    # See if an item of the same Price was already added and add up quantities in it's the case
    try:
        # TODO: Could be a problem if the same Price was added manually through admin
        i = OrderItem.objects.get(order=o, product=p)
        i.quantity = i.quantity + float(quantity)
        i.save()
    except ObjectDoesNotExist:
        i = OrderItem()
        i.order = o
        i.quantity = float(quantity)
        i.product = p
        i.save()

    # Check for final quantity, delete if 0 or negative
    if i.quantity <= 0:
        i.delete()
        return JsonResponse({'success': True, 'message':_((u'Sacamos <strong>%s</strong> del carrito de compras') % (p.product.name))})

    return JsonResponse({'success': True, 'message':_((u'Ahora tenés %d <strong>%s</strong> en el carrito de compras') % (i.quantity, p.product.name))})

@login_required
def user_confirmed_tf(request):
    customer = request.user.customer
    customer.last_confirmed_tf = datetime.today()
    customer.save()
    return JsonResponse({'success': True})
