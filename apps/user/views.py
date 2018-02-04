from rest_framework import viewsets, filters, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.views import APIView

from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer
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
        recommend = User.objects.all()[:10]
        data = UserSerializer(recommend, many=True).data
        return Response(data)


class UserSearch(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, user_name, format=None):
        user = User.objects.get(username=user_name)
        data = UserSerializer(user).data
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
