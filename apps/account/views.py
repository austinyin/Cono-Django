import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

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
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'login': True, 'user': SelfSerializer(user, context={'request': request}).data})

        return HttpResponseForbidden({'login': False})


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


@csrf_exempt
def change_password_view(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        if user.is_active and user.check_password(data['oldPassword']) and user.check_password(
                data['newPassword']) == user.check_password(data['newPasswordRepeat']):
            user.set_password(user.check_password(data['newPassword']))
            return JsonResponse(
                {'changePassword': True, 'user': SelfSerializer(user, context={'request': request}).data})
        return HttpResponseForbidden({'changePassword': False})
