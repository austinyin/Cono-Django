from django.urls import re_path

from Cono.urls import router
from . import views

def regist():
    router.register(r'tweetImage', views.TweetImageViewSet, "tweetimage")



urlpatterns = [
    re_path(r'tranfer$', views.transfer_upload_view),
    re_path(r'commit$', views.pub_commit_view)
]

