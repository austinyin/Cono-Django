from django.urls import re_path

from Cono.urls import router
from . import views

def regist():
    router.register(r'tweetImage', views.TweetImageViewSet, "tweetimage")



urlpatterns = [
    re_path(r'transfer$', views.transfer_upload_view),
    re_path(r'transfer/reset$', views.transfer_reset_view),
    re_path(r'transfer/imageRemove$', views.pub_image_remove_view),
    re_path(r'commit$', views.pub_commit_view),
]

