import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from apps.relation.models import Comment, TweetRelations, PersonRelations, CommentSign
from apps.relation.serializers import CommentSerializer
from apps.tweet.models import Tweet
from apps.tweet.serializers import TweetSerializer
from apps.user.models import User
from apps.user.serializers import UserSerializer
from shared.constants.common import TweetRelationType, PersonUserRelationType, NoticesType, notices_set


@csrf_exempt
def leave_comment_view(request):
    """
    tweet添加评论
    """
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            user = request.user

            tweet_obj = Tweet.objects.get(id=post_data['tweetId'])
            text = post_data['text']
            if tweet_obj is not None:
                # 评论对象创建
                comment_obj = Comment.objects.create(
                    tweet=tweet_obj,
                    user=user,
                    text=text
                )

                # comment notice添加
                notices_set(tweet_obj.user, NoticesType['comments'], comment_obj)

                new_tweet = Tweet.objects.get(id=post_data['tweetId'])
                # 评论标记对象创建
                sign_target_list = post_data['signTargetList']
                if sign_target_list:
                    for target in sign_target_list:
                        target_obj = User.objects.get(username=target)

                        comment_sign_obj = CommentSign.objects.create(
                            act_one=user,
                            target_one=target_obj,
                            comment=comment_obj,
                            text=text
                        )

                        # commentSign notice添加
                        notices_set(target_obj, NoticesType['commentSigns'], comment_sign_obj)

                # 将request 传给 TweetSerializer 以便获取登陆用户
                return JsonResponse({
                    'leaveComment': True,
                    'tweet': TweetSerializer(new_tweet, context={'request': request}).data,
                    'comment': CommentSerializer(comment_obj, context={'request': request}).data
                })

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
            comment_id = post_data['commentId']
            comment_obj = Comment.objects.get(id=comment_id)
            if comment_obj is not None:
                comment_obj.delete()
                new_tweet = Tweet.objects.get(id=post_data['tweetId'])
                context = {'request': request}

                return JsonResponse({'removeComment': True,
                                     'tweet': TweetSerializer(new_tweet, context=context).data,
                                     'commentId': comment_id
                                     })

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

        try:
            post_data = json.loads(request.body)
            user = request.user
            tweet_obj = Tweet.objects.get(id=post_data['tweetId'])
            tweet_relations_obj = TweetRelations.objects.get_or_create(
                user=user,
                tweet=tweet_obj,
            )[0]
            if tweet_relations_obj is not None:
                if post_data['type'] == TweetRelationType['like']:
                    tweet_relations_obj.is_like = bool(not tweet_relations_obj.is_like)

                    # like notice添加
                    notices_set(tweet_obj.user, NoticesType['tweetLikes'], tweet_relations_obj)

                if post_data['type'] == TweetRelationType['collect']:
                    tweet_relations_obj.is_collect = bool(not tweet_relations_obj.is_collect)

                tweet_relations_obj.save()
                new_tweet = Tweet.objects.get(id=post_data['tweetId'])
                context = {'request': request}
                return JsonResponse(
                    {'tweetRelationSet': True, 'tweet': TweetSerializer(new_tweet, context=context).data})

        except Exception as e:
            print(e)
            return HttpResponseServerError({
                'tweetRelationSet': False,
            })


@csrf_exempt
def person_relation_set_view(request):
    """
    personRelation 设置
    """
    if request.method == 'POST':

        try:
            post_data = json.loads(request.body)
            user = request.user if request.user.is_active else None
            target_id = post_data['targetId']
            target = User.objects.get(id=target_id)
            person_relations_obj = PersonRelations.objects.get_or_create(
                act_one=user,
                target_one=target
            )[0]
            if post_data['type'] == PersonUserRelationType['follow']:
                person_relations_obj.is_follow = bool(not person_relations_obj.is_follow)

                # follow notice添加
                notices_set(target, NoticesType['personFollows'], person_relations_obj)

            elif post_data['type'] == PersonUserRelationType['block']:
                person_relations_obj.is_block = bool(not person_relations_obj.is_block)

            person_relations_obj.save()
            new_target = User.objects.get(id=target_id)
            return JsonResponse({'personRelationSet': True,
                                 'user': UserSerializer(new_target, context={'request': request}).data})

        except Exception as e:
            print(e)
            return HttpResponseServerError({
                'personRelationSet': False,
            })
