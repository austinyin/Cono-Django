import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from apps.user.models import User
from apps.user.serializers import UserSerializer


@csrf_exempt
def regist_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.create(
                username=data['username'],
                password=data['password'],
                fullname=data['fullname']
            )
        except:
            return HttpResponseForbidden({'regist': False})
        if user is not None:
            return JsonResponse({'regist': True, 'user': UserSerializer(user).data})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'login': True, 'user': UserSerializer(user).data})
        return HttpResponseForbidden({'login': False})


@csrf_exempt
def login_check_view(request):
    if request.method == 'POST':
        user = request.user
        if user is not None and user.is_active:
            return JsonResponse({'loginCheck': True, 'user': UserSerializer(user).data})
        return JsonResponse({'loginCheck': False, 'user': {}})


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        try:
            logout(request)
        except:
            return HttpResponseForbidden({'logout': False})
        return JsonResponse({'logout': True})
