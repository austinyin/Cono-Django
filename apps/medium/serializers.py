from django.db import InternalError
from rest_framework import serializers

from apps.medium.models import TweetFileTransfer, TweetImage
from apps.relation.models import Comment, TweetRelations
from apps.relation.serializers import CommentSerializer, TweetRelationsSerializer
from apps.tweet.models import Tweet
from apps.user.models import User
from apps.user.serializers import UserSimpleSerializer


class TweetFileTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetFileTransfer
        fields = '__all__'
        depth = 1


class TweetImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TweetImage
        fields = '__all__'
