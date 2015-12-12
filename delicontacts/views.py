from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required

from deliverest.decorators import render_to
from delicontacts.models import Customer

@render_to('account_settings.html')
def new_account_settings(request, *args, **kwargs):
    partial_pipeline = request.session.get('partial_pipeline')
    if partial_pipeline is None:
        # Redirect to home if we are not in an auth pipeline
        return redirect('home')

    # Get user_id from session
    user_id = partial_pipeline['kwargs']['user']
    user = get_user_model().objects.get(pk=user_id)

    CustomerForm = modelform_factory(Customer, fields=('address', 'phone', 'prefered_delivery_method'))

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

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            backend = request.session['partial_pipeline']['backend']
            return redirect('social:complete', backend=backend)
    else:
        form = CustomerForm(instance=customer)

    return {'form': form}

@login_required
@render_to('account_settings.html')
def account_settings(request, *args, **kwargs):
    if not hasattr(request.user, 'customer'):
        return redirect('social:begin', backend='facebook')
    customer = request.user.customer

    CustomerForm = modelform_factory(Customer, fields=('address', 'phone', 'prefered_delivery_method'))
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerForm(instance=customer)

    return {'form': form}