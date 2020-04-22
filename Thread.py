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
from googletrans import Translator
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')


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
                currentPag_html = requests.get(urls[i], headers=headers, timeout=20)  # 访问该网站
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
    enddingSingle = QtCore.pyqtSignal(str,str)
    def __init__(self,urls,title,savepath):
        self.urls=urls
        self.title=title
        self.savepath=savepath
        super(getartThread, self).__init__()

    def run(self):
        self.messageSingle.emit("正在建立连接...")
        chrome_options = webdriver.ChromeOptions()
        # prefs = {"download.default_directory": "C:/Users/ENERGY/Desktop/download",
        #          "download.prompt_for_download": False, }
        # chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--auto-open-devtools-for-tabs");
        chrome_options.add_argument(
            "user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36")
        client = webdriver.Chrome(chrome_options=chrome_options)
        # 如果没有把chromedriver加入到PATH中,就需要指明路径 executable_path='/home/chromedriver'
        print(len(self.urls))
        for url in self.urls:
            self.messageSingle.emit("正在访问服务器...")
            try:
                client.get(url)
            except Exception as a:
                # self.messageSingle.emit("当前线路连接失败，正在切换线路...（"+str(a)+"）")
                # print("当前线路连接失败，正在切换线路...（"+str(a)+"）")
                # continue
                self.messageSingle.emit("当前线路连接超时，请更新线路信息！")
                print("当前线路连接超时，请更新线路信息！（"+str(a)+"）")
                return
            # time.sleep(5)
            self.messageSingle.emit("正在解析...")
            try:
                client.find_element_by_xpath("//input[@name='request']").send_keys(self.title)
                # time.sleep(1)
                client.find_element_by_xpath("//div[@id='open']").click()
                pdfurl = client.find_element_by_xpath("//body//iframe[1]").get_attribute('src')
            except Exception as a:
                self.messageSingle.emit("文章不存在!")
                print("网站解析失败，请联系李臣浩进行升级...（"+str(a)+"）")
                return
            self.messageSingle.emit("正在保存文件...")
            try:
                self.title
                rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
                self.title = re.sub(rstr, "_", self.title)  # 替换为下划线
                if len(self.title)>120:
                    self.title=self.title[0:120]

                if not os.path.exists(self.savepath):
                    os.makedirs(self.savepath)
                filename=self.savepath+"/" + self.title + ".pdf"
                print(filename)
                urllib.request.urlretrieve(pdfurl, filename)
            except Exception as a:
                self.messageSingle.emit("文件保存失败（"+str(a)+"）")
                print("文件保存失败（"+str(a)+"）")
            self.messageSingle.emit("文件保存成功！")
            print("文件保存成功！")
            # time.sleep(3)
            # 关闭谷歌浏览器
            # content = client.page_source
            client.close()
            client.quit()
            break
        self.enddingSingle.emit(self.savepath,self.title + ".pdf")


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