from django.conf.urls import include, url
from hotline import views as hotline_views


urlpatterns = (
    # Examples:
    url(r'lastscan/$', hotline_views.lastscan, name='lastscan'),
    url(r'get_category/$', hotline_views.get_category, name='get_category'),
    url(r'get_category_data/$', hotline_views.get_category_data, name='get_category_data'),
    url(r'scan_it/$', hotline_views.scan_it, name='scan_it'),
    url(r'get_status/$', hotline_views.get_status, name='get_status'),
    url(r'^savecat/(?P<id>[0-9]+)/$', hotline_views.savecat, name='savecat'),
    url(r'^getprice/(?P<id>[0-9]+)/$', hotline_views.getprice, name='getprice'),
    url(r'^get_not_active/(?P<id>[0-9]+)/$', hotline_views.get_not_active, name='get_not_active'),
)
