from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^add$', views.add),
    url(r'^add_interest$', views.add_interest),
    url(r'^users$', views.users),
    url(r'^login$', views.login),
    url(r'^show/(?P<id>\d+)$', views.show),
]
