import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from apps.medium.models import TweetImage, TweetFileTransfer
from apps.medium.serializers import TweetFileTransferSerializer, TweetImageSerializer
from apps.tweet.models import Tweet
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
        file_type = 1
        transfer_obj = TweetFileTransfer.objects.get_or_create(short_code=short_code)[0]
        transfer_obj.type = file_type
        try:
            if file_type == UploadMediaType['image']:
                image = TweetImage(image=file)
                image.save()
                transfer_obj.images.add(image)
            if file_type == UploadMediaType['video']:
                transfer_obj.video = file
            response = JsonResponse({'transferUpload': True,
                                     'transferObj': TweetFileTransferSerializer(transfer_obj,
                                                                                context=serializer_context).data})
            response.set_cookie('shortCode', short_code)
            return response
        except Exception as e:
            print(e)
            transfer_obj.delete()
            return JsonResponse({'transferUpload': False})


@csrf_exempt
def pub_commit_view(request):
    if request.method == 'POST':
        short_code = request.COOKIES['shortCode']
        transfer_obj = TweetFileTransfer.objects.get(short_code=short_code)
        tweet = Tweet()
        if transfer_obj.type == UploadMediaType['image']:
            tweet.images = transfer_obj.images
            tweet.type = UploadMediaType['image']
        if transfer_obj.type == UploadMediaType['video']:
            tweet.video = transfer_obj.video
            tweet.type = UploadMediaType['video']
        data = request.POST
        tweet.text = data['text']
        tweet.short_code = short_code
        tweet.save()
        response = JsonResponse({'pubCommit': True, 'short_code': short_code})
        response.set_cookie('shortCode', None)
        return response


class TweetImageViewSet(viewsets.ModelViewSet):
    queryset = TweetImage.objects.all()
    serializer_class = TweetImageSerializer
