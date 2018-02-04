from django.conf.urls import re_path

from . import views

urlpatterns = [
    re_path(r'login$', views.login_view),
    re_path(r'regist$', views.regist_view),
]
