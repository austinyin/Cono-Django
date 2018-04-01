from django.utils import timezone
from django.forms import model_to_dict
from rest_framework import serializers

from apps.relation.models import PersonRelations, Notices
from apps.tweet.models import Tweet
from apps.user.models import User, Visitor
from apps.relation.serializers import PersonRelationsSerializer
from shared.constants.common import NoticesType


class UserSerializerTweetTotalMixin(serializers.ModelSerializer):
    tweet_total = serializers.SerializerMethodField()

    def get_tweet_total(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            tweet_list = Tweet.objects.filter(user=user)
            return len(tweet_list)


class UserSerializerRelationObjMixin(serializers.ModelSerializer):
    relations_obj = serializers.SerializerMethodField()

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


class UserSerializer(serializers.ModelSerializer):
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


class SearchUserSerializer(UserSerializerTweetTotalMixin, UserSerializerRelationObjMixin):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions')


class SelfSerializer(UserSerializerTweetTotalMixin, UserSerializerRelationObjMixin):
    notices = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions')

    def get_notices(self, obj):
        request = self.context['request']
        user = request.user
        if user is None or not user.is_active:
            return

        notices_obj = Notices.objects.get_or_create(user=user)[0]

        ret_list = []
        # 为UserModel的Key
        seria_key_list = ['user', 'act_one', 'target_one']

        # first for: 获得筛选后的 notices_obj中manytomany对象列表
        # second for: model_to_dict() from obj to obj_dict
        # third for: 将包含User对象的key的value设置为UserSerializer(User).data
        # return { 'type': key,'obj': obj_dict}
        for key in NoticesType.keys():
            relation_child_list = getattr(notices_obj, key)
            filter_list = relation_child_list.filter(update_time__lt=timezone.datetime.now()).reverse()

            for obj in filter_list:
                obj_dict = model_to_dict(obj)
                obj_dict['update_time'] = obj.update_time  # model_to_dict 会排除auto_now=True等字段

                # 遍历将dict中的value为user id的value设置为Serializer后的user data
                for seria_key in seria_key_list:
                    if seria_key in obj_dict:
                        seri_user = User.objects.get(id=obj_dict[seria_key])
                        obj_dict[seria_key] = UserSerializer(seri_user, context={'request': request}).data

                ret_list.append({
                    'type': key,
                    'obj': obj_dict
                })

        return ret_list


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
