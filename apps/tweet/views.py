from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseServerError, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.relation.models import Comment
from apps.relation.serializers import CommentSerializer
from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer
from shared.modelApply.paginators import StandardResultSetPagination


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = StandardResultSetPagination

    @detail_route(methods=['get'])
    def thumbnail(self, request, pk=None):
        thumbnail_image = self.get_object().image_thumbnail.image
        print('thumbnail_image',thumbnail_image)
        return HttpResponse(thumbnail_image, content_type="image/png")


class RecommendTweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-create_time')
    serializer_class = TweetSerializer
    pagination_class = StandardResultSetPagination


class TweetCommentsView(APIView):
    def get(self, request, id, format=None):
        try:
            tweet = Tweet.objects.get(id=int(id))
            comment_list = Comment.objects.filter(tweet=tweet)
            page = request.GET.get('page')
            paginator = Paginator(comment_list, 10)
            comments = paginator.page(page)
            data = {
                'hasNext': comments.has_next(),
                'data': CommentSerializer(comments[:10], many=True).data,
            }
            return Response(data)
        except Exception as e:
            print(e)
            return HttpResponseServerError({'tweetCommentNextPage': False, })
