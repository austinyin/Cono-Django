from apps.user import urls as user_urls
from apps.tweet import urls as tweet_urls
from apps.medium import urls as medium_urls

def registAll():
    user_urls.regist()
    tweet_urls.regist()
    medium_urls.regist()