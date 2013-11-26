from django.conf.urls import patterns, include, url
import userprofile.urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', include(userprofile.urls)),
	url(r'^auth/$', include(userprofile.urls)),
	url(r'^user_panel/$', include(admin.site.urls)),
	url(r'^invalid/$', include(userprofile.urls)),
	url(r'^register/$', include(userprofile.urls)),
	url(r'^admin/', include(admin.site.urls)),
)
