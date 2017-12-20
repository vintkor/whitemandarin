# encoding: utf-8
from django.conf.urls import url

from profile import views as profile_views

urlpatterns = [
    url(r'^$', profile_views.profile, name='profile'),
    url(r'^addtowishlist/$', profile_views.addtowishlist , name='addtowishlist'),
    url(r'^viewed/$', profile_views.viewed , name='viewed'),
    url(r'^addaction/$', profile_views.addaction , name='addaction'),
    url(r'^settings/$', profile_views.settings , name='settings'),
    url(r'^whishlist/$', profile_views.whishlist , name='whishlist'),
    url(r'^orders/$', profile_views.orders , name='orders'),
    url(r'^order/(?P<id>[0-9]+)/$', profile_views.order, name='order'),

]
