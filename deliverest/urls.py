
"""Deliverest URL definitions."""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^$', 'deliorders.views.home',
        name="home"),
    url(r'^categoria/(?P<category>[^/]+)/$',
        'deliorders.views.home', name="category"),
    url(r'^agregar/$',
        'deliorders.views.add_to_cart', name="add_to_cart"),
    url(r'^agregar-producto/$',
        'deliorders.views.add_dialog', name="add_dialog"),
    url(r'^carrito/$',
        'deliorders.views.cart', name="shopping_cart"),
    url(r'^confirmar-carrito/$',
        'deliorders.views.confirm_cart', name="confirm_cart"),
    url(r'^estado-carrito/$',
        'deliorders.views.cart_status', name="cart_status"),
    url(r'^confirm-tf/$',
        'deliorders.views.user_confirmed_tf', name="confirm_tf"),

    url(r'^buscar/$',
        'deliproducts.views.search_ajax', name="product_search_ajax"),

    url(r'^cuenta/$',
        'delicontacts.views.account_settings', name="account_settings"),
    url(r'^nueva-cuenta/$',
        'delicontacts.views.new_account_settings',
        name="new_account_settings"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Auth views
    url('^', include('django.contrib.auth.urls')),

    # Social login related
    url(r'^logout/$', 'deliorders.views.logout'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
