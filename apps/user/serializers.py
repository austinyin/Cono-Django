from django.utils import timezone
from django.forms import model_to_dict
from rest_framework import serializers

from apps.relation.models import PersonRelations, Notices
from apps.tweet.models import Tweet
from apps.user.models import User, Visitor
from apps.relation.serializers import PersonRelationsSerializer
from shared.constants.common import NoticesType

UserSerializerTypes = {
    "common": 1,
    "selfCenter": 2,
}


class UserSerializerTweetTotalMixin(serializers.ModelSerializer):
    tweet_total = serializers.SerializerMethodField()

    def get_tweet_total(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            tweet_list = Tweet.objects.filter(user=user)
            print('tweet_list', tweet_list)
            return len(tweet_list)


class UserSerializerRelationObjMixin(serializers.ModelSerializer):
    tweet_total = serializers.SerializerMethodField()
    relations_obj = serializers.SerializerMethodField()

    def get_tweet_total(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            tweet_list = Tweet.objects.filter(user=user)
            print('tweet_list', tweet_list)
            return len(tweet_list)


    def get_relations_obj(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            friend_list = []
            block_list = []
            follower_list = []
            relation_list = PersonRelations.objects.filter(act_one=user)
            target_relation_list = PersonRelations.objects.filter(target_one=user)

            for relation in relation_list:
                user = relation.target_one
                if relation.is_follow:
                    friend_list.append(user)
                if relation.is_block:
                    block_list.append(user)

            for relation in target_relation_list:
                user = relation.target_one
                if relation.is_follow:
                    follower_list.append(user)

            relations_obj = {
                "friendList": UserSerializer(friend_list, many=True).data,
                "blockList": UserSerializer(block_list, many=True).data,
                "followerList": UserSerializer(follower_list, many=True).data
            }

            return relations_obj


class UserSerializer(UserSerializerTweetTotalMixin):
    relations = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions')

    def get_relations(self, obj):
        try:
            user = self.context['request'].user
            if user is not None:
                relations = PersonRelations.objects.get_or_create(act_one=user, target_one=obj)[0]
                return PersonRelationsSerializer(relations).data
        except Exception as e:
            print(e)
            return {}


class UserCenterUserSerializer(UserSerializerRelationObjMixin):
    relations = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions')

    def get_relations(self, obj):
        try:
            user = self.context['request'].user
            if user is not None:
                relations = PersonRelations.objects.get_or_create(act_one=user, target_one=obj)[0]
                return PersonRelationsSerializer(relations).data
        except Exception as e:
            print(e)
            return {}



class SelfSerializer(UserSerializerRelationObjMixin):
    notices = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions')

    def get_notices(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            notices_obj = Notices.objects.get_or_create(user=user)[0]
            list = []
            for key in NoticesType.keys():
                a = getattr(notices_obj, key)
                filter_list = a.filter(update_time__lt=timezone.datetime.now())
                for obj in filter_list:
                    list.append({
                        'type': key,
                        'obj': model_to_dict(obj)
                    })
            return list


# def notice_filter(obj):



class UserSimpleSerializer(serializers.ModelSerializer):
    relations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'fullname', 'relations']

    def get_relations(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            relations = PersonRelations.objects.get_or_create(act_one=user, target_one=obj)[0]
            return PersonRelationsSerializer(relations).data
        return []


class UserMinimalismSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'
