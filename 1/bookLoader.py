# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import io


class BookLoader:
    def __init__(self, service, book):
        self.service = service
        self.book = book
        self.chapters = []

    def getChapters(self):
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
        return title, text

    def writer(self, path, title, text):
        write_flag = True
        with io.open(path, 'a', encoding='utf-8') as f:
            f.write((title + '\n').decode("utf-8"))
            f.writelines(text.decode("utf-8"),)
            f.write('\n\n'.decode("utf-8"),)


if __name__ == '__main__':
    service = 'http://www.biqukan.com'
    book = 'http://www.biqukan.com/1_1094/'
    target = 'http://www.biqukan.com/1_1094/5403177.html'
    path = "1094.txt"

    bookLoader = BookLoader(service, book)
    bookLoader.getChapters()
    length = len(bookLoader.chapters)
    index = 0
    print("开始下载...%s" % (length))
    for chapter in bookLoader.chapters:
        title, text = bookLoader.getChapter(chapter)
        bookLoader.writer(path, title, text)
        index += 1
        os.system('clear')
        print("下载%.3f%%..." % (float(index) / length * 100) + '\r')

    print("下载完成！")
