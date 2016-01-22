# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required

from deliverest.decorators import render_to
from delicontacts.models import Customer

@login_required
@render_to('account_settings.html')
def account_settings(request, *args, **kwargs):
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
    else:
        customer = user.customer

    CustomerForm = modelform_factory(Customer, fields=('address', 'phone', 'prefered_delivery_method'))
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm(instance=customer)

    return {'form': form}