from django.forms import model_to_dict
from rest_framework import serializers

from apps.relation.models import Comment, TweetRelations
from apps.user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ('tweet',)


class TweetRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetRelations
        fields = ['is_like', 'is_collect']
