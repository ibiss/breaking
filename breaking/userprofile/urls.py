from django.conf.urls import *
from userprofile.views import home
from userprofile.views import auth_view
from userprofile.views import user_panel
from userprofile.views import invalid_login
from userprofile.views import register_user
from userprofile.views import account
from userprofile.views import generate

urlpatterns = patterns('',
	url(r'^$', home),
        url(r'^auth/', auth_view),
        url(r'^user_panel/', user_panel),
        url(r'^invalid/', invalid_login),
        url(r'^register/', register_user),
	url(r'^generate/', generate),
        url(r'^account/', account),
)
