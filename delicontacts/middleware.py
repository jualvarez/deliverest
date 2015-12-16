from django.shortcuts import redirect, render

from allauth.account.views import confirm_email, email
from allauth.account.models import EmailAddress

from delicontacts.views import account_settings


class AssociateUserToCustomerMiddleware(object):
	def process_view(self, request, view_func, view_args, view_kwargs):
		excluded_views = [
			account_settings,
			email,
			confirm_email
		]
		if view_func in excluded_views:
			return
		if request.user.is_authenticated():
			if request.user.is_staff:
				return
			if not EmailAddress.objects.filter(user=request.user,
			                                   verified=True).exists():
			    return render(request,
			                  'account/verified_email_required.html')

			if not hasattr(request.user, 'customer'):
				return redirect('account_settings')

