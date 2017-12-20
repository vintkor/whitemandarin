from django.conf.urls import include, url
from comments import views as comments_views

urlpatterns = [
     url(r'^save/$', comments_views.comment_save, name='comment_save'),
     url(r'^save_answer/$', comments_views.save_answer, name='save_answer'),
     url(r'^utility/$', comments_views.utility, name='utility'),
]
