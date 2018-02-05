# -*- coding: utf-8 -*-

"""Deliverest URL definitions."""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from delicontent.views import page
from delicontacts.views import account_settings, delete_account
from deliorders.views import home, search, add_to_cart, load_order, add_dialog, cart, confirm_cart, cart_status, user_confirmed_tf
from deliproducts.views import price, search_ajax

from deliproducts.sitemaps import sitemaps


urlpatterns = [
    url(r'^$', home,
        name="home"),
    url(r'^categoria/(?P<category>[^/]+)/$',
        home, name="category"),
    url(r'^buscar/$',
        search, name="search"),
    url(r'^agregar/$',
        add_to_cart, name="add_to_cart"),
    url(r'^agregar-producto/$',
        add_dialog, name="add_dialog"),
    url(r'^producto/(?P<id>[^/]+)$',
        price, name="price_redir"),
    url(r'^productos/(?P<slug_id>[^/]+)$',
        price, name="price"),
    url(r'^pagina/(?P<slug>[^/]+)$',
        page, name="page"),
    url(r'^recargar-pedido/$',
        load_order, name="load_order"),
    url(r'^canasta/$',
        cart, name="shopping_cart"),
    url(r'^confirmar-canasta/$',
        confirm_cart, name="confirm_cart"),
    url(r'^estado-canasta/$',
        cart_status, name="cart_status"),
    url(r'^confirm-tf/$',
        user_confirmed_tf, name="confirm_tf"),

    url(r'^buscar-ajax/$',
        search_ajax, name="product_search_ajax"),

    url(r'^cuenta/$',
        account_settings, name="account_settings"),
    url(r'^cuenta/(?P<mode>[^/]+)/$',
        account_settings, name="account_settings_mode"),
    url(r'^borrarcuenta/$',
        delete_account, name="account_delete"),

    url(r'^markdownx/', include('markdownx.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    # Robots.txt
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),


    # Auth views
    url('^', include('django.contrib.auth.urls')),

    # Social login related
    url(r'^accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        })
    ]
