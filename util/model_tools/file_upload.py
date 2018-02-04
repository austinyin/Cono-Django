# 上传路径

# 公共公共路径
def common_upload_path_handler(instance, filename):
    return "{main}/{id}/{file}".format(main=instance._meta.verbose_name, id=instance.id,
                                           file=filename)

