from django.shortcuts import redirect

def associate_customer(backend, user, response, *args, **kwargs):
	if hasattr(user, 'customer'):
		return None
	else:
		# Redirect to account settings page
		return redirect('new_account_settings')