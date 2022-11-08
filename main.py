from random import shuffle
from util.crawl import crawl
from util.video_maker import video_maker
from util.merge import merge_video
def get_random_words(words_path, total=20):
    with open(words_path, 'r') as f:
        words = f.readlines()
        shuffle(words)
        ret = []
        for i in range(total):
            now = words[i]
            if now[len(now)-1] == '\n':
                now = now[:len(now)-1]
            ret.append(now)
        return ret

if __name__ == '__main__':
    rate = 0
    words = get_random_words('./words')
    print(words)
    for word in words:
        c = crawl(word)
        c.crawl()
        rate = rate+1
        print(rate, '/61 crawl', word, 'success')

        vm = video_maker(word, True)
        vm.make_video()
        rate = rate+1
        print(rate, '/61 make with cn', word, 'success')

        vm2 = video_maker(word, False)
        vm2.make_video()
        rate = rate+1
        print(rate, '/61 make without cn', word, 'success')

    merge_video('./workspace', 1)
