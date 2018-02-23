from django.db import InternalError
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.relation.models import Comment, TweetRelations, TweetSign
from apps.relation.serializers import CommentSerializer, TweetRelationsSerializer

from apps.tweet.models import Tweet
from apps.user.models import User
from apps.user.serializers import UserSimpleSerializer


class TweetSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['images', 'video', 'type','id']
        depth = 1


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    total_like = serializers.SerializerMethodField()
    sign_list = serializers.SerializerMethodField()
    relations = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = '__all__'
        depth = 1

    def get_user(self, obj):
        # 这里将context进行了中转
        return UserSimpleSerializer(obj.user, context={'request': self.context['request']}).data

    def get_total_like(self, obj):
        likes = TweetRelations.objects.filter(tweet=obj, is_like=1)
        return len(likes)

    def get_comments(self, obj):
        comments = Comment.objects.filter(tweet=obj).order_by('-create_time')
        hasNext = True if len(comments) > 10 else False
        data = {
            'hasNext': hasNext,
            'data': CommentSerializer(comments[:10], many=True).data,
        }
        return data

    def get_relations(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            relations = TweetRelations.objects.get_or_create(user=user, tweet=obj)[0]
            if relations is not None:
                return TweetRelationsSerializer(relations).data
        return []

    def get_sign_list(self, obj):
        sign_list = TweetSign.objects.filter(tweet=obj)
        sign_target_list = [sign.target_one for sign in sign_list]
        return [model_to_dict(item)['username'] for item in sign_target_list]
