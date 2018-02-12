from django.urls import re_path

from Cono.urls import router
from apps.tweet import views


def regist():
    router.register(r'tweet', views.TweetViewSet)
    router.register(r'recommendTweet', views.RecommendTweetViewSet)
