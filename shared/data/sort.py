from apps.tweet.models import Tweet


def sortUserListBylatestPubDateKey(obj):
    tweetList = Tweet.objects.filter(user=obj)
    if tweetList:
        return tweetList[0].update_time


def excludeObjFilter():
    pass