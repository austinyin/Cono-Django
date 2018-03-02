
from django.utils import timezone


def common_upload_path_handler(instance, filename):
    now = timezone.now().strftime("%Y/%m/%d")
    return "./{main}/{time}/{file}".format(main=instance._meta.verbose_name,time=now,file=filename)





