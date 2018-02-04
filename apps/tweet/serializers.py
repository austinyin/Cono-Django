from django.db import InternalError
from rest_framework import serializers

from apps.relation.models import Comment, TweetRelations
from apps.relation.serializers import CommentSerializer, TweetRelationsSerializer
from apps.tweet.models import Tweet
from apps.user.models import User
from apps.user.serializers import UserSimpleSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    total_like = serializers.SerializerMethodField()
    relations = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_user(self, obj):
        return UserSimpleSerializer(obj.user).data

    def get_total_like(self, obj):
        likes = TweetRelations.objects.filter(tweet=obj, is_like=1)
        return len(likes)

    def get_comments(self, obj):
        comments = Comment.objects.filter(tweet=obj).order_by('-create_time')
        return CommentSerializer(comments, many=True).data

    def get_relations(self, obj):
        user = User.objects.get(username='monkyin')
        relations = TweetRelations.objects.filter(user=user, tweet=obj)
        if relations:
            return TweetRelationsSerializer(relations[0]).data
        else:
            return {}

