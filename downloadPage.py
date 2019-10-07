#-*-coding:utf-8-*-

import requests
import os
from bs4 import BeautifulSoup
from urllib import parse
import re
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

class Complex(QWebEngineView):
    def __init__(self, url):
        from PyQt5.QtWidgets import QApplication
        import sys
        from PyQt5.QtCore import QUrl
        import lxml.html

        self.html = ''
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self):
        self.page().toHtml(self.callable)

    def callable(self, data):
        self.html = data
        self.app.quit()


class Download():

    replaces = {}

    def download_htmlcssjs(self,filepath,content):
        try:
            fo = open(filepath, "w",encoding='utf-8')
            fo.write(content)
            fo.close()
        finally:
            pass
        pass


    def multiple_replace(self,text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))
        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)


    def download_image(self,filepath,iter_content):
        try:
            with open(filepath, 'wb') as f:
                for chunk in iter_content(chunk_size=1024):  # 历遍请求下载回来的图片
                    if chunk:  # 如果chunk不等于0
                        f.write(chunk)
                        f.flush()  # 刷新缓冲区
                f.close()
        finally:
            pass
        pass

    #处理
    #content
    def dealList(self, lists, contentType, url, cate, target):
        for c in lists:
            #计算绝对路径
            realfilepath = parse.urljoin(url, c.get(target))
            #图片采用steam
            if (contentType != "img"):
                req = requests.get(realfilepath)
            else:
                req = requests.get(realfilepath, stream=True)
            req.encoding = self.encoding
            if(req.status_code==200):
                filenameDict = parse.urlparse(realfilepath)
                filename = str(filenameDict[2]).replace("/","")
                if c.get(target) != None:
                    self.replaces[c.get(target)] = "static/" + contentType + "/" + filename
                if(filename):
                    if(contentType!="img"):
                        self.download_htmlcssjs(cate + "/static/" + contentType + "/" + filename, req.text)
                    else:
                        self.download_image(cate + "/static/" + contentType + "/" + filename,req.iter_content)


    #下载整个网页
    def __init__(self, url, cate, model="simple"):
        if(model=="complex"):
            r = Complex(url)
            content = r.html
            # 偷个懒，用requests抓取到的编码做ajax加载页面的编码
            request = requests.get(url)
            self.encoding = request.apparent_encoding
        else:
            request = requests.get(url)
            request.encoding = request.apparent_encoding
            self.encoding = request.apparent_encoding
            content = request.text


        paths = ['img','css','js']
        for p in paths:
            ps = cate + "/static/" + p
            if not os.path.exists(cate + "/static/" + p):
                os.makedirs(cate+"/static/" + p)
        soup = BeautifulSoup(request.text, "lxml")
        csss = soup.findAll('link')
        jss = soup.findAll('script')
        imgs = soup.findAll('img')
        self.dealList(csss, "css", url, cate, "href")
        self.dealList(jss, "js", url, cate, "src")
        self.dealList(imgs, "img", url, cate, "src")

        print(self.replaces)
        try:
            fo = open(cate+"/index.html", "w", encoding=self.encoding)
            fo.write(self.multiple_replace(content, self.replaces) )
            fo.close()
        finally:
            pass
        pass
