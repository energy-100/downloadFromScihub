import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import re
import pickle
import os
import datetime
import requests
import urllib
import PyPDF2
from docx import Document
import urllib3
from googletrans import Translator
from bs4 import BeautifulSoup
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# urllib3.disable_warnings()
# requests.packages.urllib3.disable_warnings()
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class artobject():
    def __init__(self, parent=None):
        self.filename = ""
        self.path = ""
        self.allpath = ""
        self.data = ""
        self.datastr = ""

        self.title = ""
        self.titlerecode = ""
        self.chinesetitle = ""
        self.extra = ""
        self.doi = ""
        self.authors = ""
        self.arturl = ""
        self.infrequesturl = ""
        self.extractpath=""
        self.transpath=""

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
            "https://sci-hub.sci-hub.hk",
            "https://sci-hub.hk",
            "https://sci-hub.la",
            "https://sci-hub.mn",
            "https://sci-hub.name",
            "https://sci-hub.is",
            "https://sci-hub.tv",
            "https://sci-hub.ws",
            "https://www.sci-hub.cn",

            "https://sci-hub.sci-hub.tw",
            "https://sci-hub.sci-hub.mn",
            "https://sci-hub.sci-hub.tv"]
        print("正在更新线路...")
        ableurls = []

        for i in range(len(urls)):
            try:
                currentPag_html = requests.get(urls[i], headers=headers, timeout=10,verify=False)  # 访问该网站
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

class updateurlsThreadsingle(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(str,float)
    def __init__(self,url,timeout):
        self.time=9999
        self.url=url
        self.timeout=timeout
        self.ableurls=[]
        super(updateurlsThreadsingle, self).__init__()
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



        print("正在更新线路...")
        try:
            if self.url in ["https://www.crossref.org/","https://translate.google.cn/"]:
                currentPag_html = requests.get(self.url, headers=headers, timeout=self.timeout,verify=False)  # 访问该网站
            else:
                testurldata={"request": "Quantum mechanics and hidden variables: A test of Bell's inequality by the measurement of the spin correlation in low-energy proton-proton scattering"}
                currentPag_html = requests.post(self.url, data=testurldata, verify=False,headers=headers, timeout=self.timeout)
                main_html = currentPag_html.text
                soup = BeautifulSoup(main_html, 'html.parser')
                pdfurl = soup.find_all('iframe')
                if len(pdfurl)==0:
                    currentPag_html.text=""
        except Exception as a:
            print(self.url + "失败！("+str(a)+")")
            # self.messageSingle.emit(self.url.split(".")[-1] +"）线路失败！  "+str(a))
            self.enddingSingle.emit(self.url, self.time)
            return
        # 先判断是否成功访问
        if currentPag_html.status_code == 200:
            if currentPag_html.text=="":
                self.time=10000
                print(self.url + "返回值为空！" + str(currentPag_html.status_code))
                # self.messageSingle.emit(self.url + "失败！" + str(currentPag_html.status_code))
            else:
                print(self.url + "成功！")
                self.time=currentPag_html.elapsed.total_seconds()
                # self.messageSingle.emit(self.url.split(".")[-1] + "线路成功！("+str(self.time)+")")
                # delay=ping_host(urls[i])
                # print(urls[i]+"成功！ 延迟：",delay)

        else:
            print(self.url + "失败！"+str(currentPag_html.status_code))
            # self.messageSingle.emit(self.url + "失败！"+str(currentPag_html.status_code))
        # if len(self.ableurls)>=1:
        #     return
        self.enddingSingle.emit(self.url,self.time)

class extractThread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal()
    progressSingle = QtCore.pyqtSignal(int)
    progressvisualSingle = QtCore.pyqtSignal(bool)
    def __init__(self,art:artobject):
        self.art=art
        super(extractThread, self).__init__()
    def run(self):
        self.progressvisualSingle.emit(True)
        self.progressSingle.emit(0)
        self.messageSingle.emit("正在进行OCR识别...")
        pdfFile = open(self.art.allpath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        # print(pdfReader.getDocumentInfo())
        # print(pdfReader.numPages)
        content=""
        for i in range(pdfReader.numPages):
            content+=pdfReader.getPage(i).extractText()
            self.progressSingle.emit(int((i+1)/pdfReader.numPages*100))
        pdfFile.close()
        document = Document()                          # 打开一个基于默认“模板”的空白文档
        document.add_heading(self.art.title, 0)      # 添加标题
        p = document.add_paragraph(content)
        try:
            path=self.art.path + "/" + self.art.titlerecode + ".docx"
            document.save(path)
        except PermissionError :
            self.progressvisualSingle.emit(False)
            self.messageSingle.emit("文件占用，请关闭后重试！")
        except Exception as e:
            self.messageSingle.emit("未知异常，请重试！("+str(e)+")")
        self.art.extractpath=path
        self.progressvisualSingle.emit(False)
        self.messageSingle.emit("文本提取完成！")
        self.enddingSingle.emit()

class transThread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal()
    progressSingle = QtCore.pyqtSignal(int)
    progressvisualSingle = QtCore.pyqtSignal(bool)
    def __init__(self,art:artobject):
        self.art=art
        super(extractThread, self).__init__()
    def run(self):
        self.progressvisualSingle.emit(True)
        self.progressSingle.emit(0)
        self.messageSingle.emit("正在翻译...")
        pdfFile = open(self.art.allpath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        # print(pdfReader.getDocumentInfo())
        # print(pdfReader.numPages)
        content=""
        for i in range(pdfReader.numPages):
            content+=pdfReader.getPage(i).extractText()
            self.progressSingle.emit(int((i+1)/pdfReader.numPages*100))
        pdfFile.close()
        document = Document()                          # 打开一个基于默认“模板”的空白文档
        document.add_heading(self.art.title, 0)      # 添加标题
        p = document.add_paragraph(content)
        try:
            path=self.art.path + "/" + self.art.titlerecode + ".docx"
            document.save(path)
        except PermissionError :
            self.progressvisualSingle.emit(False)
            self.messageSingle.emit("文件占用，请关闭后重试！")
        except Exception as e:
            self.messageSingle.emit("未知异常，请重试！("+str(e)+")")
        self.art.extractpath=path
        self.progressvisualSingle.emit(False)
        self.messageSingle.emit("文本提取完成！")
        self.enddingSingle.emit()



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

        self.messageSingle.emit("正在请求数据...")
        try:
            # title = "Quantum mechanics and hidden variables: A test of Bell's inequality by the measurement of the spin correlation in low-energy proton-proton scattering"
            url = "https://search.crossref.org/?q=" + self.title +"&page="+str(self.page)
            currentPag_html = requests.get(url, headers=headers, timeout=100,verify=False)  # 访问该网站
        except Exception as a:
            self.messageSingle.emit("请求数据错误（"+str(a)+")")
            return
        try:
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
                else:
                    artobjecttemp.chinesetitle="翻译线路超时！"
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
        except Exception as a:
            self.messageSingle.emit("解析数据错误（"+str(a)+")")
            return
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
        filepath=""
        try:
            self.messageSingle.emit("正在建立连接...")
            # scihuburl = self.scihuburl+"/" + self.art.doi
            # scihub_html = requests.get(scihuburl, headers=headers, timeout=20)  # 访问该网站
            scihub_html = requests.post(self.scihuburl,{"request":self.art.title},headers=headers, verify = False)
            # scihub_html = requests.post(self.scihuburl,{"request":self.art.title})
            print(scihub_html.status_code)
            main_html = scihub_html.text
            soup = BeautifulSoup(main_html, 'html.parser')
            identifyingcode=soup.find_all('captcha')
            if len(identifyingcode)>0:
                print("验证码")
                imageurl=identifyingcode[0]['src']
                res = requests.get(imageurl,verify=False)
                img = QImage.fromData(res.content)

                self.codeimageSingle.emit(img)

            # pdfurl = soup.find('iframe')['src']

            pdfurl = soup.find_all('iframe')
            if len(pdfurl)==0:
                print("self.scihuburl",self.scihuburl)
                self.messageSingle.emit("sci-hub未收录此文章，无法下载！")
                return
            rstr = r"[\/\\\:\*\?\"\<\>\|]"
            filename=re.sub(rstr, "_", self.art.title)
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            filepath=self.path+"/"+filename+".pdf"
            self.messageSingle.emit("正在下载...（由于网络问题可能会消耗较长时间）")

            if pdfurl[0]['src'][0:4]!="http":
                pdfurl2="https:"+pdfurl[0]['src']
            else:
                pdfurl2 = pdfurl[0]['src']
            print(pdfurl2)
            self.progressSingle.emit(0)
            self.progressvisualSingle.emit(True)
            urllib.request.urlretrieve(pdfurl2, filepath,self.Schedule)
            self.progressvisualSingle.emit(False)
            self.art.filename = self.art.title+".pdf"
            self.art.titlerecode = filename
            self.art.path = self.path
            self.art.allpath = filepath
            self.art.data = datetime.datetime.now()
            self.art.datastr = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
            self.messageSingle.emit("文章下载成功！")
            self.enddingSingle.emit(self.art)
        except PermissionError:
            print("self.scihuburl", self.scihuburl)
            print("文章下载失败！（文件占用，请关闭pdf文件后尝试下载)")  # 或者加入其它判断条件
            self.messageSingle.emit("文章下载失败！（文件占用，请关闭pdf文件后尝试下载)")
        except Exception as a :
            print(repr(a))
            print("self.scihuburl", self.scihuburl)
            self.messageSingle.emit("文章下载失败！（"+str(a)+")")
            self.progressvisualSingle.emit(False)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as a:
                    pass

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

class getauthoritythread(QThread):
    messageSingle = QtCore.pyqtSignal(str)
    enddingSingle = QtCore.pyqtSignal(str)
    def __init__(self,enstr):
        self.enstr = enstr
        super(getauthoritythread, self).__init__()
    def run(self):
        translator = Translator()
        chineseword=translator.translate(self.enstr, dest='zh-CN').text
        self.enddingSingle.emit(chineseword)