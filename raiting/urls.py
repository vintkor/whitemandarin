from django.conf.urls import include, url

from raiting import views as raiting_views


urlpatterns = (    # Examples:
    url(r'(?P<paket>[-a-z0-9_]+)/(?P<model_name>[-A-Za-z0-9_]+)/(?P<item_id>\d+)/$', raiting_views.reit, name='reit'),
)
