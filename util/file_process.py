import os
import subprocess

from PIL import Image

from Cono.settings import BASE_DIR


def ffmpeg_video_screenshot(video_path, save_path):
    ffmpeg_path = os.path.join(BASE_DIR, 'extra_apps/ffmpeg/ffmpeg.exe')
    print('ffmpeg_path', ffmpeg_path)
    img_crop_cmd = '{} -ss 00:00:02 -i {} -frames:v 1 -s 300x300 {}'.format(ffmpeg_path, video_path, save_path)
    img_crop_pipe = subprocess.Popen(img_crop_cmd, shell=True)
    img_crop_pipe.wait()
    return save_path


# 这里还是使用的之前写的算法,效率很低，需要改动。
def image_scale(size, file_path, save_path,afterRemove=False):
    width = size[0]
    height = size[1]
    infile = file_path

    im = Image.open(infile)
    scale = width / height
    scale_width, scale_height, fi_height, fiwidth = 1, 1, 1, 1
    while scale_width < im.size[0]:
        if scale_height == scale_width / scale:
            fiwidth = scale_width
            fi_height = scale_height
        scale_width += 1
        scale_height = scale_width / scale

    hori, verti = (im.size[0] / 2, im.size[1] / 2)
    box = (hori - fiwidth / 2, verti - fi_height / 2, hori + fiwidth / 2, verti + fi_height / 2)
    region = im.crop(box)

    region.thumbnail((width, height), Image.ANTIALIAS)
    region.save(save_path)
    # 是否需要删除
    if afterRemove:
        os.remove(infile)

    return save_path



