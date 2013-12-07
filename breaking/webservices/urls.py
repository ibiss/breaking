from django.conf.urls import patterns, url, include
from rest_framework import routers
from webservices import views

router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^mission/(?P<id>[^/]+)/$', views.TaskViewList.as_view()),
    url(r'^login/(?P<username>[^/]+)/$', views.LoginUser.as_view()),
)
