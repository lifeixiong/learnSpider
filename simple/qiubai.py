# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import io

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
}


class QiuBai:
    def __init__(self, service):
        self.service = service
        self.blocks = []
        self.articles = []

    def getContent(self):
        req = requests.get(url=self.service, headers=headers)
        req.encoding = 'utf-8'
        html = req.text
        bf = BeautifulSoup(html)
        self.blocks = bf.find_all("div", class_="article")

    def getArticle(self, block):
        author = block.find("h2").text
        text = block.find("div", class_="content").span.text
        print(author, text)
        return author, text

    def writer(self, path, title, text):
        write_flag = True
        with io.open(path, 'a', encoding='utf-8') as f:
            f.write((title + u'\n'))
            f.writelines(text)
            f.write(u'\n')


if __name__ == '__main__':
    service = 'https://www.qiushibaike.com/'
    path = "qiubai.txt"

    qiuBai = QiuBai(service)
    qiuBai.getContent()
    length = len(qiuBai.blocks)
    index = 0
    print("开始下载...%s" % (length))
    for block in qiuBai.blocks:
        title, text = qiuBai.getArticle(block)
        qiuBai.writer(path, title, text)
        index += 1
        os.system('clear')
        print("下载%.2f%%..." % (float(index) / length * 100) + '\r')

    print("下载完成！")
