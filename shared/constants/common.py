from apps.relation.models import Notices

UploadMediaType = {
    'image': 1,
    'video': 2,
}

TweetRelationType = {
    'like': 1,
    'collect': 2,
}

PersonUserRelationType = {
    'follow': 1,
    'block': 2,
}

NoticesType = {
    'comments': "comments",
    'commentSigns': "commentSigns",
    'tweetSigns': "tweetSigns",
    'tweetLikes': "tweetLikes",
    'personFollows': "personFollows",
}

# NoticeKeyToSerializer = {
#     'comments': CommentSerializer,
#     'commentSigns': CommentSignSerializer,
#     'tweetSigns': "tweetSigns",
#     'tweetLikes': "tweetLikes",
#     'personFollows': "personFollows",
# }

IMAGE_THUMBNAIL_SIZE = (300, 300)
IMAGE_THUMBNAIL_TYPE = 'jpg'

def notices_set(user,type, item):
    try:
        notices_obj = Notices.objects.get_or_create(user=user)[0]
        getattr(notices_obj, NoticesType[type]).add(item)
    except Exception as e:
        print(e)
