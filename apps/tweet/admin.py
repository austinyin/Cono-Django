from django.contrib import admin

from .models import Tweet,TweetImage,TweetVideo

admin.site.register(Tweet)
admin.site.register(TweetImage)
admin.site.register(TweetVideo)