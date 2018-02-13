from django.forms import model_to_dict
from rest_framework import serializers

from apps.relation.models import Comment, TweetRelations, PersonRelations


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ('tweet',)


class TweetRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetRelations
        fields = ['is_like', 'is_collect']


class PersonRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRelations
        fields = ['is_follow', 'is_block']
