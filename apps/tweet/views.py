from rest_framework import viewsets

from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

