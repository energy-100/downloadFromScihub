import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import re
import pickle
import os
import datetime
import math
import threading
import time
from pyquery import PyQuery as pq
import requests
import numpy as np
from ping3 import ping
from selenium import webdriver
import urllib
import json
from googletrans import Translator
from bs4 import BeautifulSoup
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

class artobject():
    def __init__(self, parent=None):
        self.filename = ""
        self.path = ""
        self.allpath = ""
        self.data = ""
        self.datastr = ""

        self.title = ""
        self.chinesetitle = ""
        self.extra = ""
        self.doi = ""
        self.authors = ""
        self.arturl = ""
        self.infrequesturl = ""

class updateurlsThread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(list)
    def __init__(self):
        self.ableurls=[]
        super(updateurlsThread, self).__init__()
    def run(self):
        '''请求头'''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }

        '''代理ip'''
        proxies = {
            "http": "http://202.121.96.33:8086",
            "http": "http://58.253.154.179:9999",
            "http": "http://163.204.243.51:9999",
            "http": "http://183.166.20.179:9999",
            "http": "http://183.166.20.179:9999",
            "http": "http://49.86.181.35:9999",

            # "https": "https://221.228.17.172:8181",

        }

        urls = [
            "https://sci-hub.tw",
            "https://sci-hub.hk",
            "https://sci-hub.la",
            "https://sci-hub.mn",
            "https://sci-hub.name",
            "https://sci-hub.is",
            "https://sci-hub.tv",
            "https://sci-hub.ws",
            "https://www.sci-hub.cn",
            "https://sci-hub.sci-hub.hk",
            "https://sci-hub.sci-hub.tw",
            "https://sci-hub.sci-hub.mn",
            "https://sci-hub.sci-hub.tv"]

        ableurls = []

        for i in range(len(urls)):
            try:
                currentPag_html = requests.get(urls[i], headers=headers, timeout=100)  # 访问该网站
            except Exception as a:
                print(urls[i] + "失败！("+str(a)+")")
                self.messageSingle.emit(urls[i].split(".")[-1] + "（"+str(i)+"/"+str(len(urls))+"）线路失败！")
                continue
            # 先判断是否成功访问
            if currentPag_html.status_code == 200:
                print(urls[i] + "成功！")
                self.messageSingle.emit(urls[i].split(".")[-1] + "线路成功！")
                # delay=ping_host(urls[i])
                # print(urls[i]+"成功！ 延迟：",delay)
                self.ableurls.append(urls[i])
            else:
                print(urls[i] + "失败！")
                self.messageSingle.emit(urls[i] + "失败！")
            if len(self.ableurls)>=1:
                break
        self.enddingSingle.emit(self.ableurls)

class getartThread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(list)
    def __init__(self,urls,title,trans,page=1):
        self.urls = urls
        self.title = title
        self.page = page
        self.trans=trans
        super(getartThread, self).__init__()

    def run(self):
        headers = {"User-Agent": "GroovyBib/1.1 (mailto:abc551218@126.com) BasedOnFunkyLib/1.4",'Connection':'close'}

        '''代理ip'''
        proxies = \
            {
            "http": "http://202.121.96.33:8086",
            "http": "http://58.253.154.179:9999",
            "http": "http://163.204.243.51:9999",
            "http": "http://183.166.20.179:9999",
            "http": "http://183.166.20.179:9999",
            "http": "http://49.86.181.35:9999",
            # "https": "https://221.228.17.172:8181",
            }

        urls = [
            "https://sci-hub.tw",
            "https://sci-hub.sci-hub.tw",
            "https://sci-hub.hk",
            "https://sci-hub.la",
            "https://sci-hub.mn",
            "https://sci-hub.name",
            "https://sci-hub.is",
            "https://sci-hub.tv",
            "https://sci-hub.ws",
            "https://www.sci-hub.cn",
            "https://sci-hub.sci-hub.hk",
            "https://sci-hub.sci-hub.mn",
            "https://sci-hub.sci-hub.tv"]

        self.messageSingle.emit("正在请求数据...")
        # title = "Quantum mechanics and hidden variables: A test of Bell's inequality by the measurement of the spin correlation in low-energy proton-proton scattering"
        url = "https://search.crossref.org/?q=" + self.title +"&page="+str(self.page)
        currentPag_html = requests.get(url, headers=headers, timeout=20)  # 访问该网站
        self.messageSingle.emit("正在解析数据...")
        main_html = currentPag_html.text
        soup = BeautifulSoup(main_html, 'html.parser')
        artitems = soup.find_all('td', class_="item-data")
        artlist=[]
        translator = Translator()
        for i,artitem in enumerate(artitems):
            self.messageSingle.emit("正在获取数据 " + str(i + 1) + "/" + str(len(artitems)))
            title=artitem.find("p",class_="lead").string
            # print(title)
            artobjecttemp = artobject()
            artobjecttemp.title = artitem.find("p", class_="lead").string.strip()
            if self.trans:
                artobjecttemp.chinesetitle = translator.translate(artobjecttemp.title, dest='zh-CN').text

            artobjecttemp.extra = artitem.find("p", class_="extra").get_text().strip().replace("\n", " ")
            authors = artitem.find("p", class_="expand")
            if authors is not None:
                artobjecttemp.authors = authors.get_text().strip().replace("\n", " ")[8:]

            arturl=artitem.find('a')['href']
            if arturl is not None:
                artobjecttemp.arturl = arturl

            if artobjecttemp.arturl !="":
                artobjecttemp.doi = artobjecttemp.arturl[16:]

            if artobjecttemp.doi !="":
                artobjecttemp.infrequesturl= "https://api.crossref.org/works/" + artobjecttemp.doi

            artlist.append(artobjecttemp)
        self.enddingSingle.emit(artlist)

        # arturl = soup.find_all('div', class_="item-links")
        # authors = soup.find_all('p', class_="expand")
        # authors = authors[0].string
        # print(authors)
        # arturl = arturl[0].find('a')['href']
        # doi = arturl[16:]
        # artinfurl = "https://api.crossref.org/works/" + doi
        # artinfjson = requests.get(artinfurl, headers=headers, timeout=20)  # 访问该网站
        # artinfdict = json.loads(artinfjson.text)
        # print(artinfdict["message"])
        # for key, value in artinfdict["message"].items():
        #     print(key, value)
        # scihuburl = "https://sci-hub.tw/" + doi
        # scihub_html = requests.get(scihuburl, headers=headers, timeout=20)  # 访问该网站
        # main_html = scihub_html.text
        # soup = BeautifulSoup(main_html, 'html.parser')
        # pdfurl = soup.find('iframe')['src']
        # urllib.request.urlretrieve(pdfurl, 'C:/Users/ENERGY/Desktop/download/555.pdf')
        # print(pdfurl)
        # self.enddingSingle.emit(self.savepath,self.title + ".pdf")

class savefilethread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(artobject)
    codeimageSingle = QtCore.pyqtSignal(QImage)
    progressSingle = QtCore.pyqtSignal(int)
    progressvisualSingle = QtCore.pyqtSignal(bool)

    def __init__(self,scihuburl:str,art:artobject,path:str):
        self.scihuburl = scihuburl
        self.art = art
        self.path = path
        super(savefilethread, self).__init__()


    def Schedule(self,a,b,c):
        #a:已经下载的数据块
        # b:数据块的大小
        #c:远程文件的大小
        per = 100.0 * a * b / c
        if per > 100 :
            per = 100
        # mess='已完成：'+ str(round(per,2)+"%%")
        # self.messageSingle.emit(mess)
        self.progressSingle.emit(int(per))


    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
        }

        '''代理ip'''
        proxies = \
            {
                "http": "http://202.121.96.33:8086",
                "http": "http://58.253.154.179:9999",
                "http": "http://163.204.243.51:9999",
                "http": "http://183.166.20.179:9999",
                "http": "http://183.166.20.179:9999",
                "http": "http://49.86.181.35:9999",
                # "https": "https://221.228.17.172:8181",
            }

        try:
            self.messageSingle.emit("正在建立连接...")
            # scihuburl = self.scihuburl+"/" + self.art.doi
            # scihub_html = requests.get(scihuburl, headers=headers, timeout=20)  # 访问该网站
            scihub_html = requests.post(self.scihuburl,{"request":self.art.title})
            main_html = scihub_html.text
            soup = BeautifulSoup(main_html, 'html.parser')
            identifyingcode=soup.find_all('captcha')
            if len(identifyingcode)>0:
                imageurl=identifyingcode[0]['src']
                res = requests.get(imageurl)
                img = QImage.fromData(res.content)

                self.codeimageSingle.emit(img)

            # pdfurl = soup.find('iframe')['src']

            pdfurl = soup.find_all('iframe')
            if len(pdfurl)==0:
                self.messageSingle.emit("sci-hub未收录此文章，无法下载！")
                return
            rstr = r"[\/\\\:\*\?\"\<\>\|]"
            filename=re.sub(rstr, "_", self.art.title)
            filepath=self.path+"/"+filename+".pdf"
            self.messageSingle.emit("正在下载...（由于网络问题可能会消耗较长时间）")
            self.progressvisualSingle.emit(True)
            urllib.request.urlretrieve(pdfurl[0]['src'], filepath,self.Schedule)
            self.progressvisualSingle.emit(False)
            self.art.filename = self.art.title+".pdf"
            self.art.path = self.path
            self.art.allpath = filepath
            self.art.data = datetime.datetime.now()
            self.art.datastr = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
            self.messageSingle.emit("文章下载成功！")
            self.enddingSingle.emit(self.art)
        except Exception as a :
            self.messageSingle.emit("文章下载失败！（"+str(a)+")")
            self.progressvisualSingle.emit(False)




class saveachethread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(list)
    def __init__(self,achepath,arts):
        self.achepath = achepath
        self.arts=arts
        super(saveachethread, self).__init__()
    def run(self):
        achefilepath, achefilename = os.path.split(self.achepath)
        if (not os.path.exists(achefilepath)):
            os.makedirs(achefilepath)
        with open(self.achepath, "wb") as file:
            pickle.dump(self.arts, file, True)


class translatethread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(str)
    def __init__(self,enstr):
        self.enstr = enstr
        super(translatethread, self).__init__()
    def run(self):
        translator = Translator()
        chineseword=translator.translate(self.enstr, dest='zh-CN').text
        self.enddingSingle.emit(chineseword)