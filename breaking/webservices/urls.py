from django.conf.urls import patterns, url, include
from rest_framework import routers
from webservices import views

router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/(?P<username>[^/]+)/$', views.LoginUser.as_view()),
    url(r'^gameinstance/(?P<player1>[^/]+)/$', views.GameInstanceViev.as_view()),
    url(r'^checkpoints/(?P<gid>[^/]+)/$', views.CheckpointsViev.as_view()),
    url(r'^acceptgame/(?P<player1>[^/]+)/(?P<cid>[^/]+)/(?P<dt>[^/]+)/$', views.AcceptGameViev.as_view()),
)
