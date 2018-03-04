from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path(r'regist$', views.regist_view),
    re_path(r'login$', views.login_view),
    re_path(r'loginCheck$', views.login_check_view),
    re_path(r'logout$', views.logout_view),
    re_path(r'change$', views.self_change_view),
    re_path(r'change/password$', views.change_password_view),
    re_path(r'change/avatar$', views.change_avatar_view),
]
