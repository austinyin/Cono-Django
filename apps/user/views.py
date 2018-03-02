from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from rest_framework import viewsets, filters, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.relation.models import PersonRelations, TweetRelations
from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer, TweetSimpleSerializer
from apps.user.models import User, Visitor
from apps.user.serializers import UserSerializer, VisitorSerializer
from shared.modelApply.paginators import StandardResultSetPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 搜索
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @list_route(methods=['get'])
    def recommend(self, request, pk=None):
        user = request.user
        if user is not None and user.is_active:
            recommend = User.objects.exclude(username=user.username)[:10]
        else:
            recommend = User.objects.all()[:10]
        data = UserSerializer(recommend, context={'request': request}, many=True).data
        return Response(data)

    @list_route(methods=['get'])
    def snapshotList(self, request, pk=None):
        """
        now版本1 找出最近发表了文章的好友,
        after 版本2 设计算法找出最近发表文章较多的好友。
        """
        user = request.user
        if user is not None and user.is_active:
            snap_list = PersonRelations.objects.filter(act_one=user)
            clean_following_user_list = []
            # 这里也可以改成for循环处理,这样缺乏可读性.
            following_user_list = [
                clean_following_user_list.append(obj.target_one)
                if Tweet.objects.filter(user=obj.target_one)
                else False for obj in snap_list
            ]
            sorted_following__user_list = sorted(
                clean_following_user_list,
                key=lambda obj: Tweet.objects.filter(user=obj)[0].create_time
            )
            return Response(UserSerializer(sorted_following__user_list[:5], many=True).data)

    @detail_route(methods=['get'])
    def relations(self, request, pk=None):
        user = request.user
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
            return Response(relations_obj)

    @detail_route(methods=['get'])
    def avatar(self, request, pk=None):
        avatar = self.get_object().avatar
        return HttpResponse(avatar, content_type="image/png")


class UserSearch(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, user_name, format=None):
        user = User.objects.get(username=user_name)
        data = UserSerializer(user, context={'request': request}).data
        # 判断是否是查询的自己，并加上相应字段。
        if user == request.user:
            data.setdefault('isSelf', True)

        return Response(data)


class UserRelationsSearch(APIView):

    def get(self, request, user_name, format=None):
        user = User.objects.get(username=user_name)
        if user.is_active:
            return redirect('/api/user/{}/relations'.format(user.id))


class UserSnapshots(APIView):

    def get(self, request, user_name, format=None):
        user = User.objects.get(username=user_name)
        if user.is_active:
            tweet_list = Tweet.objects.filter(user=user).order_by('-update_time')[:5]
            return Response(TweetSimpleSerializer(tweet_list,many=True).data)
        else:
            return HttpResponseForbidden({'UserSnapshots': False})


class UserTweetList(generics.ListAPIView):
    serializer_class = TweetSerializer
    lookup_url_kwarg = "user_name"
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        user_name = self.kwargs.get(self.lookup_url_kwarg)
        user = User.objects.get(username=user_name)
        tweets = Tweet.objects.filter(user=user)
        return tweets


class UserCollectTweetList(generics.ListAPIView):
    serializer_class = TweetSerializer
    lookup_url_kwarg = "user_name"
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        user_name = self.kwargs.get(self.lookup_url_kwarg)
        user = User.objects.get(username=user_name)
        tweetRelations_objects = TweetRelations.objects.filter(user=user,is_collect=True)
        tweets = [obj.tweet for obj in tweetRelations_objects]
        return tweets


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


