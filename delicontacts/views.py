# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required

from deliverest.decorators import render_to
from delicontacts.models import Customer
from deliorders.models import Order
from delidelivery.models import DeliveryMethod


@login_required
@render_to('account_settings.html')
def account_settings(request, *args, **kwargs):
    mode = kwargs.get('mode', 'settings')
    valid_modes = ['settings', 'orders']
    if mode not in valid_modes:
        raise ValueError("Mode '%s' does does not apply to this view" % (mode))
    user = request.user
    if not hasattr(user, 'customer'):
        try:
            # Associate the customer to the user if we can find it
            customer = Customer.objects.filter(email=user.email)[0]
            customer.associated_user = user
        except IndexError:
            # Fill out customer info from social data
            customer = Customer()
            customer.associated_user = user
            customer.name = user.first_name + ' ' + user.last_name
            customer.email = user.email
            customer.new = True
    else:
        customer = user.customer

    CustomerForm = modelform_factory(Customer, fields=('name', 'address', 'phone', 'prefered_delivery_method'))
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        form.fields['prefered_delivery_method'].queryset = DeliveryMethod.objects.filter(is_active=True)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm(instance=customer)
        form.fields['prefered_delivery_method'].queryset = DeliveryMethod.objects.filter(is_active=True)

    current_order = Order.objects.get_active(customer)
    can_add = current_order and current_order.status

    return {
        'form': form,
        'customer': customer,
        'mode': mode,
        'can_add': can_add
    }


@login_required
@render_to('delete_confirm.html')
def delete_account(request, *args, **kwargs):
    confirm = request.POST.get('confirm', False)
    if confirm == '1':
        from django.contrib.auth import logout
        request.user.delete()
        logout(request)
        return {
            'confirmed': True
        }
    return {
        'confirmed': False
    }
