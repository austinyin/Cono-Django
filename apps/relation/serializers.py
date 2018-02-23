from django.forms import model_to_dict
from rest_framework import serializers

from apps.relation.models import Comment, TweetRelations, PersonRelations, CommentSign


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    sign_list = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('tweet',)

    def get_sign_list(self, obj):
        sign_list = CommentSign.objects.filter(comment=obj)
        sign_target_list = [sign.target_one for sign in sign_list]
        # 只需返回username即可
        return [model_to_dict(item)['username'] for item in sign_target_list]


class TweetRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetRelations
        fields = ['is_like', 'is_collect']


class PersonRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRelations
        fields = ['is_follow', 'is_block']


# class RelationCommentSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     sign_list = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Comment
#         fields = '__all__'
#
#
# class RelationCommentSignSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommentSign
#         fields = '__all__'
#         depth = 1

