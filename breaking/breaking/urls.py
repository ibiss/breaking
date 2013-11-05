from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'breakingapp.views.home'),
	url(r'^auth/$', 'breakingapp.views.auth_view'),
	url(r'^user_panel/$', 'breakingapp.views.user_panel'),
	url(r'^invalid/$', 'breakingapp.views.invalid_login'),
    # url(r'^breaking/', include('breaking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
