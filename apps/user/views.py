from rest_framework import viewsets, filters, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.views import APIView

from apps.relation.models import PersonRelations
from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer
from apps.user.models import User, Visitor
from apps.user.serializers import UserSerializer, VisitorSerializer
from shared.data.sort import sortUserListBylatestPubDateKey
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
        data = UserSerializer(recommend, context={'request': request},many=True).data
        return Response(data)

    @list_route(methods=['get'])
    def snapshotList(self, request, pk=None):
        user = request.user
        if user is not None and user.is_active:
            snap_list = PersonRelations.objects.filter(act_one=user)
            clean_following_user_list = []
            # 这里有点脏.
            following_user_list = [clean_following_user_list.append(obj.target_one) if Tweet.objects.filter(user=obj.target_one) else False for obj in snap_list]
            sorted_following__user_list = sorted(clean_following_user_list,
                                           key = lambda obj: Tweet.objects.filter(user=obj)[0].create_time)
            print('sorted_following_List',sorted_following__user_list)
            return Response(UserSerializer(sorted_following__user_list[:5],many=True).data)


class UserSearch(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, user_name, format=None):
        user = User.objects.get(username=user_name)
        data = UserSerializer(user,context={'request': request}).data
        # 判断是否是查询的自己，并加上相应字段。
        if user == request.user:
            data.setdefault('isSelf', True)

        return Response(data)


class UserTweetList(generics.ListAPIView):
    serializer_class = TweetSerializer
    lookup_url_kwarg = "user_name"
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        user_name = self.kwargs.get(self.lookup_url_kwarg)
        user = User.objects.get(username=user_name)
        tweets = Tweet.objects.filter(user=user)
        return tweets


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
