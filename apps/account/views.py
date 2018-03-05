import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseForbidden,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from apps.user.models import User
from apps.user.serializers import SelfSerializer


@csrf_exempt
def regist_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.create(
                username=data['username'],
                password=make_password(data['password']),  # 加密
                fullname=data['fullname']
            )
        except:
            return HttpResponseForbidden({'regist': False})
        if user is not None:
            return JsonResponse({'regist': True, 'user': SelfSerializer(user, context={'request': request}).data})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data['username'],data['password'])
        print(data['username'],data['password'])
        print(data['username'],data['password'])
        user = authenticate(username=data['username'], password=data['password'])
        print('user',user)
        print('user',user)
        print('user',user)
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'login': True, 'user': SelfSerializer(user, context={'request': request}).data})

        return HttpResponseBadRequest({'login': False})


@csrf_exempt
def login_check_view(request):
    if request.method == 'POST':
        user = request.user
        if user is not None and user.is_active:
            return JsonResponse({'loginCheck': True, 'user': SelfSerializer(user, context={'request': request}).data})

        return JsonResponse({'loginCheck': False, 'user': {}})


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        try:
            logout(request)
        except:
            return HttpResponseForbidden({'logout': False})

        return JsonResponse({'logout': True})


# class SelfChangeView(APIView):
#     def post(self, request, format=None):
#         print('request')
#         user = request.user
#         data = json.loads(request.body)
#         if user.is_active:
#             for k, v in data.items():
#                 value = v['value']
#                 if value:
#                     setattr(user, k, value)
#             user.save()
#             return JsonResponse({"selfChange": True, "user": SelfSerializer(user, context={'request': request}).data})


@csrf_exempt
def self_change_view(request):
    if request.method == 'POST':
        print('request.META',request.META)
        user = request.user
        data = json.loads(request.body)
        if user.is_active:
            for k, v in data.items():
                value = v['value']
                if value:
                    setattr(user, k, value)
            user.save()
            return JsonResponse({"selfChange": True, "user": SelfSerializer(user, context={'request': request}).data})


@csrf_exempt
def change_avatar_view(request):
    if request.method == 'POST':
        print(request.COOKIES)
        user = request.user
        print('request.FILES',request.FILES)
        file = request.FILES['file']
        if user.is_active:
            user.avatar = file
            user.save()
            return JsonResponse({"changeAvatar": True, "user": SelfSerializer(user, context={'request': request}).data})


@csrf_exempt
def change_password_view(request):
    if request.method == 'POST':
        try:
            user = request.user
            data = json.loads(request.body)
            [old_password,new_password,new_password_reapeat] = [
                data['oldPassword']['value'],
                data['newPassword']['value'],
                data['newPasswordRepeat']['value']
            ]
            print(old_password,new_password,new_password_reapeat)
            if user.is_active and user.check_password(old_password) and new_password==new_password_reapeat:
                user.set_password(user.check_password(data['newPassword']))
                return JsonResponse(
                    {'changePassword': True, 'user': SelfSerializer(user, context={'request': request}).data})
            return HttpResponseBadRequest({'changePassword': False})
        except AttributeError:
            return HttpResponseBadRequest({'changePassword': False})
