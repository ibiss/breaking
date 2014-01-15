from django.conf.urls import patterns, include, url
import userprofile.urls
import webservices.urls
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'userprofile.views.home'),
	url(r'^auth/', 'userprofile.views.auth_view'),
	url(r'^user_panel/', 'userprofile.views.user_panel'),
	url(r'^invalid/', 'userprofile.views.invalid_login'),
	url(r'^register/', 'userprofile.views.register_user'),
	url(r'^admin/', include(admin.site.urls)),
        url(r'^account/', 'userprofile.views.account'),
	url(r'^generate/', 'userprofile.views.generate'),
	url(r'^maps/', 'userprofile.views.maps'),
        url(r'^webservices/', include(webservices.urls)),
) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
