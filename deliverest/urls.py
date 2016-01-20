
"""Deliverest URL definitions."""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from deliorders.views import home, add_to_cart, add_dialog, cart, confirm_cart, cart_status, user_confirmed_tf
from deliproducts.views import search_ajax
from delicontacts.views import account_settings

urlpatterns = [
    url(r'^$', home,
        name="home"),
    url(r'^categoria/(?P<category>[^/]+)/$',
        home, name="category"),
    url(r'^agregar/$',
        add_to_cart, name="add_to_cart"),
    url(r'^agregar-producto/$',
        add_dialog, name="add_dialog"),
    url(r'^carrito/$',
        cart, name="shopping_cart"),
    url(r'^confirmar-carrito/$',
        confirm_cart, name="confirm_cart"),
    url(r'^estado-carrito/$',
        cart_status, name="cart_status"),
    url(r'^confirm-tf/$',
        user_confirmed_tf, name="confirm_tf"),

    url(r'^buscar/$',
        search_ajax, name="product_search_ajax"),

    url(r'^cuenta/$',
        account_settings, name="account_settings"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Auth views
    url('^', include('django.contrib.auth.urls')),

    # Social login related
    url(r'^accounts/', include('allauth.urls')),
    #url(r'', include('social.apps.django_app.urls', namespace='social'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
