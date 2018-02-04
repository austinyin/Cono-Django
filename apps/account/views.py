from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

import json

# def my_view(request):
#     user = authenticate(username='monkyin', password='qweqwe123')
#     if user is not None:
#         login(request, user)
#         request.session['loginUser'] = user.username
#         return JsonResponse({'login': user.username})
from apps.user.models import User
from apps.user.serializers import UserSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                return HttpResponseForbidden
        return JsonResponse(UserSerializer(user).data)


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
            return HttpResponseForbidden
        if user is not None:
            return JsonResponse(UserSerializer(user).data)
