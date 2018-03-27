# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests


class BookLoader:
    def __init__(self, service, book):
        self.service = service
        self.book = book
        self.chapters = []

    def getBookChapters(self):
        req = requests.get(url=self.book)
        html = req.text
        bf = BeautifulSoup(html)
        links = bf.find_all('dd')

        for link in links:
            self.chapters.append(link.select("a")[0].get('href'))

    def getChapter(self, link):
        target = self.service + link
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html)
        title = bf.find_all('h1')[0].text.encode("utf-8")
        texts = bf.find_all('div', class_='showtxt')
        text = texts[0].text.encode("utf-8").replace('\xa0'*8, '\n\n')
        return title + "\n\n" + text

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

    def start(self):
        self.getBookChapters()
        for chapter in self.chapters:
            text = self.getChapter(chapter)
            print(text)




if __name__ == '__main__':
    service = 'http://www.biqukan.com'
    book = 'http://www.biqukan.com/1_1094/'
    target = 'http://www.biqukan.com/1_1094/5403177.html'

    bookLoader = BookLoader(service, book)
    bookLoader.start()
