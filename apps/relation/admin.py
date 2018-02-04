from django.contrib import admin

from .models import Comment,TweetSign,TweetRelations,PersonRelations

admin.site.register(Comment)
admin.site.register(TweetSign)
admin.site.register(TweetRelations)
admin.site.register(PersonRelations)
