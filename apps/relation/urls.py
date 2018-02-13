from django.urls import re_path

from Cono.urls import router
from . import views



urlpatterns = [
    re_path(r'leaveComment$', views.leave_comment_view),
    re_path(r'removeComment$', views.remove_comment_view),
    re_path(r'tweet', views.tweet_relation_set_view),
    re_path(r'person', views.person_relation_set_view),
]

