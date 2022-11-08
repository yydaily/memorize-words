from util.file_handler import file_handler
import requests
from bs4 import BeautifulSoup
soundmark = {
    'ŋ': '\\textipa{N}',
    'ɡ': '\\textipa{g}', 'ʌ': '\\textipa{2}',
    'θ': '\\textipa{T}', 'ɒ': '\\textipa{6}',
    'ð': '\\textipa{D}', 'ɜ': '\\textipa{3}',
    'ʃ': '\\textipa{S}', 'ɑ': '\\textipa{A}', 'a': '\\textipa{A}',
    'ʒ': '\\textipa{Z}', 'ɔ': '\\textipa{O}',
    'ɪ': '\\textipa{I}', 'ə': '\\textipa{@}',
    'ʊ': '\\textipa{U}', 'ː': '\\textipa{:}',

    'ˈ': '\\textipa{"}',
    'dʒ': '\\textdyoghlig',
}

class crawl():
    def __init__(self, key):
        self.key_ = key
        self.fh_ = file_handler('./workspace/' + key)

    def crawl_soup(self):
        url = 'https://www.youdao.com/result?word=' + str(self.key_) + '&lang=en'
        ret = requests.get(url)
        self.beautiful_soup=BeautifulSoup(ret.text,'html.parser')

    def get_cn(self):
        resp = []
        for word_exp in self.beautiful_soup.find_all("li", class_="word-exp"):
            sub = ''
            pos = word_exp.find_all("span", class_="pos")
            if len(pos) == 1:
                sub = pos[0].text + ' '
            else:
                continue

            trans = word_exp.find_all("span", class_="trans")
            if len(trans) == 1:
                means = trans[0].text
                split_index = means.find('；')
                if split_index != -1:
                    means = means[:split_index]
                sub = sub + means
            sub.replace('<', '$<$')
            sub.replace('>', '$>$')
            resp.append(sub)
        self.fh_.wrap_list_to_file('cn', resp)

    def get_pronunciation(self):
        pronun = self.beautiful_soup.find_all("div", class_="phone_con")
        if len(pronun) != 1:
            return
        pronunciations = []
        for pro_nun in pronun[0].find_all("div", class_="per-phone"):
            if len(pro_nun.find_all("span")) != 2:
                continue
            pronunciation = pro_nun.find_all("span")[1].text
            sub = ''
            for index in range(len(pronunciation)):
                if pronunciation[index] in soundmark:
                    sub += soundmark[pronunciation[index]]
                elif index+1<len(pronunciation) and (pronunciation[index] + pronunciation[index+1]) in soundmark:
                    sub += soundmark[pronunciation[index] + pronunciation[index+1]]
                    index+=1
                else:
                    sub += pronunciation[index]
            pronunciations.append(sub)
        self.fh_.wrap_list_to_file('pronun', pronunciations)

    def crawl_voice(self):
        url = 'https://dict.youdao.com/dictvoice?audio='+ self.key_ + '&type=1'
        ret = requests.get(url)
        self.fh_.write_file('en.mp3', ret.content, 'wb')
        url = 'https://dict.youdao.com/dictvoice?audio=' + self.key_ + '&type=2'
        ret = requests.get(url)
        self.fh_.write_file('am.mp3', ret.content, 'wb')

    def crawl(self):
        self.crawl_soup()
        self.get_cn()
        self.get_pronunciation()
        self.crawl_voice()

if __name__ == '__main__':
    c = crawl('test')
    c.crawl_voice()
    c.crawl_soup()
    c.get_cn()
    c.get_pronunciation()


