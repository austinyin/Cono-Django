import json
import os

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from pymysql import IntegrityError
from rest_framework import viewsets

from apps.medium.models import TweetImage, TweetFileTransfer, TweetVideo
from apps.medium.serializers import TweetFileTransferSerializer, TweetImageSerializer
from apps.relation.models import TweetSign
from apps.tweet.models import Tweet
from apps.user.models import User
from shared.constants.common import UploadMediaType


def add_short_code():
    MYDIR = os.path.dirname(__file__)

    with open(os.path.join(MYDIR, 'short.txt'), 'r') as f:
        a = f.read()

    with open(os.path.join(MYDIR, 'short.txt'), 'w') as f:
        f.write(str(int(a) + 1))
    return a


@csrf_exempt
def transfer_upload_view(request):
    if request.method == 'POST':
        # 防止HyperLinkSerializer序列化错误
        serializer_context = {
            'request': request,
        }

        # 每次pub_commit的时候会清空cookie的shortCode，所以会自动更换新的shortCode。
        try:
            short_code = request.COOKIES['shortCode']

        except Exception as e:
            print(e)
            short_code = add_short_code()

        file = request.FILES['file']

        if str(file).endswith('.mp4'):
            file_type = UploadMediaType['video']
        else:
            file_type = UploadMediaType['image']
        transfer_obj = TweetFileTransfer.objects.get_or_create(short_code=short_code)[0]
        transfer_obj.type = file_type

        try:
            if file_type == UploadMediaType['image']:
                image = TweetImage(image=file)
                image.save()
                transfer_obj.images.add(image)

            if file_type == UploadMediaType['video']:
                video_obj = TweetVideo.objects.create(
                    video=file
                )
                transfer_obj.video = video_obj

            transfer_obj.save()
            response = JsonResponse({'transferUpload': True,
                                     'transferObj': TweetFileTransferSerializer(transfer_obj,
                                                                                context=serializer_context).data})
            response.set_cookie('shortCode', short_code)
            return response

        except Exception as e:
            print(e)
            transfer_obj.delete()
            return HttpResponseForbidden({'transferUpload': False})


@csrf_exempt
def pub_image_remove_view(request):
    """
    删除tranferObj指定的图片，并返回删除后的tranferObj。
    """
    if request.method == 'POST':

        try:
            tweet_image_id = int(json.loads(request.body)['id'])
            transfer_obj = TweetFileTransfer.objects.get(short_code=request.COOKIES['shortCode'])
            tweet_image_obj = TweetImage.objects.get(id=tweet_image_id)
            transfer_obj.images.remove(tweet_image_obj)
            return JsonResponse({
                'transferImageRemove': True,
                'transferObj': TweetFileTransferSerializer(transfer_obj).data
            })

        except Exception as e:
            print(e)
            return HttpResponseForbidden({
                'transferImageRemove': False,
            })





@csrf_exempt
def pub_commit_view(request):
    if request.method == 'POST':
        print("in"*10)
        post_data = json.loads(request.body)
        short_code = request.COOKIES['shortCode']
        transfer_obj = TweetFileTransfer.objects.get(short_code=short_code)
        # 先创建tweet对象， 再根据type相应赋值。
        tweet_data = {
            'short_code': short_code,
            'user': request.user,
            'text': post_data['text'],
        }
        tweet = Tweet.objects.create(**tweet_data)

        if transfer_obj.type == UploadMediaType['image']:
            for image in transfer_obj.images.all():
                tweet.images.add(image)
            tweet.type = UploadMediaType['image']

        if transfer_obj.type == UploadMediaType['video']:
            tweet.video = transfer_obj.video
            tweet.type = UploadMediaType['video']

        # 这里的save在model中进行了加工，会自动保存略缩图
        tweet.save_with_thumbnail()

        # 增加tweetSign 对象
        signs = post_data['signTargetList']
        for target_username in signs:
            target = User.objects.get(username=target_username)
            if target is not None and target.is_active:
                TweetSign.objects.create(
                    act_one=request.user,
                    target_one=target,
                    text=post_data['text'],
                    tweet=tweet
                )

        response = JsonResponse({'pubCommit': True, 'short_code': short_code})
        # 清除shortCode Cookie, 删除中转对象。
        response.delete_cookie('shortCode')
        transfer_obj.delete()
        return response

        # try:
        #     if transfer_obj.type == UploadMediaType['image']:
        #         for image in transfer_obj.images.all():
        #             tweet.images.add(image)
        #         tweet.type = UploadMediaType['image']
        #
        #     if transfer_obj.type == UploadMediaType['video']:
        #         tweet.video = transfer_obj.video
        #         tweet.type = UploadMediaType['video']
        #
        #     # 这里的save在model中进行了加工，会自动保存略缩图
        #     tweet.save_with_thumbnail()
        #
        #     # 增加tweetSign 对象
        #     signs = post_data['signTargetList']
        #     for target_username in signs:
        #         target = User.objects.get(username=target_username)
        #         if target is not None and target.is_active:
        #             TweetSign.objects.create(
        #                 act_one=request.user,
        #                 target_one=target,
        #                 text=post_data['text'],
        #                 tweet=tweet
        #             )
        #
        #     response = JsonResponse({'pubCommit': True, 'short_code': short_code})
        #     # 清除shortCode Cookie, 删除中转对象。
        #     response.delete_cookie('shortCode')
        #     transfer_obj.delete()
        #     return response
        # except Exception as e:
        #     print(e)
        #     tweet.delete()
        #     return HttpResponseForbidden({'pubCommit': False})


@csrf_exempt
def transfer_reset_view(request):
    """
    清空 tranferObj,删除关联对象,并返回执行结果。
    """
    if request.method != 'POST':
        return

    try:
        print("in"*10)
        transfer_obj = TweetFileTransfer.objects.get(short_code=request.COOKIES['shortCode'])
        if transfer_obj.type == UploadMediaType['image']:
            for tweet_image_obj in transfer_obj.images.all():
                transfer_obj.images.remove(tweet_image_obj)
                tweet_image_obj.delete()
        if transfer_obj.type == UploadMediaType['video']:
            transfer_obj.video.delete()

        return JsonResponse({
            'transferReset': True,
            'transferObj': TweetFileTransferSerializer(transfer_obj).data
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            'transferReset': False,
            'msg': 'tranferObj无需清空'
        })



class TweetImageViewSet(viewsets.ModelViewSet):
    queryset = TweetImage.objects.all()
    serializer_class = TweetImageSerializer
