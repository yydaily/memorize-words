import os
import moviepy.editor as mov
from datetime import datetime

def get_time():
    now = datetime.now()
    return str(now.year) + '-' + str(now.month) + '-' + str(now.day)

def merge_video(path, video_type=1):
    merge_video = []
    for root, dirs, files in os.walk(path):
        sub_video = [None] * 2
        for file in files:
            if not file.endswith('.mp4'):
                continue
            if video_type % 2 == 1 and file.endswith('-1.mp4'):
                sub_video[0] = mov.VideoFileClip(root + '/' + file)
            if video_type % 4 >= 2 and file.endswith('-0.mp4'):
                sub_video[1] = mov.VideoFileClip(root + '/' + file)
        if sub_video[0]:
            merge_video.append(sub_video[0])
        if sub_video[1]:
            merge_video.append(sub_video[1])
    mvs = mov.concatenate_videoclips(merge_video)
    mvs.write_videofile('./' + get_time() + '.mp4', audio_codec='aac', codec='libx264', logger=None)
