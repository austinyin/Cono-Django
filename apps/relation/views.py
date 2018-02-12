import json

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from apps.relation.models import Comment, TweetRelations
from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer
from shared.constants.common import TweetRelationType


@csrf_exempt
def leave_comment_view(request):
    """
    tweet添加评论
    """
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            tweet = Tweet.objects.get(id=post_data['tweetId'])
            if tweet is not None:
                comment_obj = Comment.objects.create(
                    tweet=tweet,
                    user=request.user,
                    text=post_data['text']
                )
                newTweet = Tweet.objects.get(id=post_data['tweetId'])
                return JsonResponse({'leaveComment': True, 'tweet': TweetSerializer(newTweet).data})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest({
                'leaveComment': False,
            })


@csrf_exempt
def remove_comment_view(request):
    """
    tweet删除评论
    """
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            comment = Comment.objects.get(id=post_data['commentId'])
            if comment is not None:
                comment.delete()
                new_tweet = Tweet.objects.get(id=post_data['tweetId'])
                return JsonResponse({'removeComment': True, 'tweet': TweetSerializer(new_tweet).data})
        except Exception as e:
            print(e)
            return HttpResponseServerError({
                'removeComment': False,
            })




@csrf_exempt
def tweet_relation_set_view(request):
    """
    tweet 喜欢和收藏关系,根据type对相应的状态取非,并返回操作后的tweet(记得save)。
    """
    if request.method == 'POST':
        post_data = json.loads(request.body)
        user = request.user
        tweet_obj = Tweet.objects.get(id=post_data['tweetId'])
        tweet_relations_obj = TweetRelations.objects.get_or_create(
            user=user,
            tweet=tweet_obj,
        )[0]
        if tweet_relations_obj is not None:
            if post_data['type'] == TweetRelationType['like']:
                print(tweet_relations_obj.is_like)
                tweet_relations_obj.is_like = bool(not tweet_relations_obj.is_like)
            elif post_data['type'] == TweetRelationType['collect']:
                tweet_relations_obj.is_collect = bool(not tweet_relations_obj.is_collect)
            tweet_relations_obj.save()
            print(tweet_relations_obj.is_like)
            new_tweet = Tweet.objects.get(id=post_data['tweetId'])
            print('pok')
            return JsonResponse({'tweetRelationSet': True, 'tweet': TweetSerializer(new_tweet).data})
        # try:
        #     post_data = json.loads(request.body)
        #     user = request.user
        #     tweet_obj = Tweet.objects.get(id=post_data['tweetId'])
        #     tweet_relations_obj = TweetRelations.objects.get_or_create(
        #         user=user,
        #         tweet=tweet_obj,
        #     )[0]
        #     if tweet_relations_obj is not None:
        #         if post_data['type'] == TweetRelationType['like']:
        #             print(tweet_relations_obj.is_like)
        #             tweet_relations_obj.is_like = bool(not tweet_relations_obj.is_like)
        #         elif post_data['type'] == TweetRelationType['collect']:
        #             tweet_relations_obj.is_collect = bool(not tweet_relations_obj.is_collect)
        #         tweet_relations_obj.save()
        #         print(tweet_relations_obj.is_like)
        #         new_tweet = Tweet.objects.get(id=post_data['tweetId'])
        #         print('pok')
        #         return JsonResponse({'tweetRelationSet': True, 'tweet': TweetSerializer(new_tweet).data})
        # except Exception as e:
        #     print(e)
        #     return HttpResponseServerError({
        #         'tweetRelationSet': False,
        #     })
