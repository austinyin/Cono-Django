from rest_framework import viewsets

from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer
from shared.modelApply.paginators import StandardResultSetPagination


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = StandardResultSetPagination


class RecommendTweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-create_time')
    serializer_class = TweetSerializer
    pagination_class = StandardResultSetPagination
