from util.file_handler import file_handler
from util.path_maker import *
import os
import cv2
from PIL import Image
import moviepy.editor as mov
class latex_maker():
    def __init__(self, key, with_cn, fh):
        self.key_ = key
        self.with_cn_ = with_cn
        self.fh_ = fh

    def get_latex_sub_path(self):
        return generate_sub_path(self.key_, self.with_cn_, '.tex')

    def get_latex_full_path(self):
        return generate_full_path(self.key_, self.with_cn_, '.tex')

    def get_pronunciation(self):
        return self.fh_.unwrap_list_from_file('pronun')

    def get_cn(self):
        return self.fh_.unwrap_list_from_file('cn')

    def gen_latex(self):
        prefix='\\documentclass{beamer}\n\\setbeamertemplate{frametitle}[default][center]\n\\mode<presentation> {\n\t\\usetheme{default}\n\t\\usecolortheme{dove}\n\t\\setbeamertemplate{navigation symbols}{}\n}\n\\usepackage{CJKutf8}\n\\usepackage{tipa}\n\\setbeamerfont{frametitle}{size=\huge}\n\\begin{document}\n\t\\begin{CJK}{UTF8}{gbsn}\n\t\t\\begin{frame}\n'
        title = '\t\t\t\\frametitle{\\ ' + self.key_ + '}\n'
        pronunciation = self.get_pronunciation()
        pronun = '\t\t\t\\begin{center}\n\t\t\t\t[' + pronunciation[0] + ']\n\n\t\t\t\t[' + pronunciation[1] + ']\n\t\t\t\\end{center}\n'
        cn = ''
        if self.with_cn_:
            cn = '\t\t\t\\begin{itemize}\n'
            for chinese in self.get_cn():
                cn += '\t\t\t\t\\item ' + chinese + '\n'
            cn += '\t\t\t\\end{itemize}\n'
        suffix='\t\t\end{frame}\n\t\end{CJK}\n\end{document}'
        self.fh_.write_file(self.get_latex_sub_path(), prefix+title+pronun+cn+suffix, 'w+')

class png_maker():
    def __init__(self, key, with_cn, lm, fh):
        self.key_ = key
        self.with_cn_ = with_cn
        self.lm_ = lm
        self.fh_ = fh

    def get_png_full_path(self):
        return generate_full_path(self.key_, self.with_cn_, '.png')

    def get_png_sub_path(self):
        return generate_sub_path(self.key_, self.with_cn_, '.png')

    def remove_file(self, suffixes):
        for suffix in suffixes:
            path = generate_sub_path(self.key_, self.with_cn_, suffix)
            if os.path.exists(path):
                os.remove(path)

    def gen_png(self):
        os.system('latex ' + self.lm_.get_latex_full_path() + ' > ./' + generate_sub_path(self.key_, self.with_cn_, '.log_ignore'))
        command = 'dvipng -D 200 ' + generate_sub_path(self.key_, self.with_cn_, '.dvi') + ' > ./' + generate_sub_path(self.key_, self.with_cn_, '.log_ignore')
        os.system(command)
        self.remove_file(['.aux', '.log', '.log_ignore', '.out', '.toc', '.dvi', '.nav', '.snm'])
        prev_path = generate_sub_path(self.key_, self.with_cn_, '1.png')
        if os.path.exists(prev_path):
            os.system('mv ' + prev_path + ' ' + self.get_png_full_path())

class video_maker():
    def __init__(self, key, with_cn):
        self.key_ = key
        self.with_cn_ = with_cn
        self.fh_ = file_handler(generate_base_path(key))

    def gen_latex(self):
        self.lm_ = latex_maker(self.key_, self.with_cn_, self.fh_)
        self.lm_.gen_latex()

    def gen_png(self):
        self.pm_ = png_maker(self.key_, self.with_cn_, self.lm_, self.fh_)
        self.pm_.gen_png()
        self.fh_.remove_file(self.lm_.get_latex_sub_path())

    def get_fake_video_full_path(self):
        return generate_full_path(self.key_, self.with_cn_, '.tmp.mp4')

    def get_fake_video_sub_path(self):
        return generate_sub_path(self.key_, self.with_cn_, '.tmp.mp4')

    def get_video_full_path(self):
        return generate_full_path(self.key_, self.with_cn_, '.mp4')

    def gen_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 20
        image = Image.open(self.pm_.get_png_full_path())
        media_writer = cv2.VideoWriter(self.get_fake_video_full_path(), fourcc, fps, image.size)
        im = cv2.imread(self.pm_.get_png_full_path())
        for i in range(fps*10):
            media_writer.write(im)
        media_writer.release()
        self.fh_.remove_file(self.pm_.get_png_sub_path())

    def add_audio(self):
        audio1 = mov.AudioFileClip(generate_base_path(self.key_) + '/en.mp3')
        audio2 = mov.AudioFileClip(generate_base_path(self.key_) + '/am.mp3')
        audio = mov.concatenate_audioclips([audio1, audio2])

        video = mov.VideoFileClip(self.get_fake_video_full_path(), verbose=False)
        video = video.subclip(audio.start, audio.end)
        video = video.set_audio(audio)
        video.write_videofile(self.get_video_full_path(), audio_codec='aac', codec='libx264', verbose=False, logger=None)
        self.fh_.remove_file(self.get_fake_video_sub_path())

    def make_video(self):
        self.gen_latex()
        self.gen_png()
        self.gen_video()
        self.add_audio()


if __name__ == '__main__':
    vm = video_maker('test', True)
    vm.make_video()
