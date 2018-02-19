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
    'comments': 'comments',
    'tweetSigns': 'tweetSigns',
    'tweetLikes': 'tweetLikes',
    'personFollows': 'personFollows',
}

def notices_set(user,list):
    try:
        for item in list:
            notices_obj = Notices.objects.get_or_create(user=user)[0]
            notices_obj[NoticesType[item.get('type')]].add(item.obj)

    except Exception as e:
        print(e)
