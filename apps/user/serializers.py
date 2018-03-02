from django.utils import timezone
from django.forms import model_to_dict
from rest_framework import serializers

from apps.relation.models import PersonRelations, Notices
from apps.user.models import User, Visitor
from apps.relation.serializers import PersonRelationsSerializer
from shared.constants.common import NoticesType


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


class SelfSerializer(serializers.ModelSerializer):
    relations_obj = serializers.SerializerMethodField()
    notices = serializers.SerializerMethodField()


    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'date_joined', 'groups', 'user_permissions')

    def get_relations_obj(self, obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            friend_list = []
            block_list = []
            relation_list = PersonRelations.objects.filter(act_one=user)
            for relation in relation_list:
                user = relation.target_one
                if relation.is_follow:
                    friend_list.append(user)
                if relation.is_block:
                    block_list.append(user)

            relations_obj = {
                "friendList": UserSerializer(friend_list, many=True).data,
                "blockList": UserSerializer(block_list, many=True).data
            }
            return relations_obj

    def get_notices(self,obj):
        user = self.context['request'].user
        if user is not None and user.is_active:
            notices_obj = Notices.objects.get_or_create(user=user)[0]
            list = []
            for key in NoticesType.keys():
                a = getattr(notices_obj,key)
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
