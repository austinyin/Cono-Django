# 上传路径
def img_upload_path_handler(instance, filename):
    return "img/{main}/{id}/{file}".format(main=instance._meta.verbose_name, id=instance.id,
                                           file=filename)