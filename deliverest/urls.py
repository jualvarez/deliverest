from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'deliorders.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^email-sent/', 'deliorders.views.validation_sent'),
    url(r'^login/$', 'deliorders.views.home'),
    url(r'^logout/$', 'deliorders.views.logout'),
    url(r'^done/$', 'deliorders.views.done', name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'deliorders.views.ajax_auth',
        name='ajax-auth'),
    url(r'^email/$', 'deliorders.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)