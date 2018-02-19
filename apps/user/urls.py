from django.conf.urls import re_path

from Cono.urls import router
from . import views

urlpatterns = [
    re_path(r'^username/(?P<user_name>.+?)/tweets', views.UserTweetList.as_view()),
    re_path(r'username/(?P<user_name>[0-9a-zA-Z]+)$', views.UserSearch.as_view()),
    re_path(r'username/(?P<user_name>[0-9a-zA-Z]+)/relations$', views.UserRelationsSearch.as_view()),
]

def regist():
    router.register(r'user', views.UserViewSet)
