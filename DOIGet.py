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
import time
from pyquery import PyQuery as pq
import requests
from bs4 import BeautifulSoup

os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

headers = {
    "User-Agent": "GroovyBib/1.1 (mailto:abc551218@126.com) BasedOnFunkyLib/1.4",
}
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
# }

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
title="Quantum mechanics and hidden variables: A test of Bell's inequality by the measurement of the spin correlation in low-energy proton-proton scattering"
url="https://search.crossref.org/?q="+title
currentPag_html = requests.get(url, headers=headers, timeout=100)  # 访问该网站
main_html = currentPag_html.text
soup = BeautifulSoup(main_html, 'html.parser')
artitems = soup.find_all('td', class_="item-data")
for artitem in artitems:
    title = artitem.find("p", class_="lead").string.strip()
    extra = artitem.find("p", class_="extra").get_text().strip().replace("\n", " ")
    authors= artitem.find("p", class_="expand").string.strip()
    arturl = artitem.find('a')['href']
    doi = arturl[16:]
    print(extra,doi)



arturl=soup.find_all('div', class_="item-links")
authors=soup.find_all('p', class_="expand")
authors=authors[0].string
print(authors)
arturl=arturl[0].find('a')['href']
doi=arturl[16:]
artinfurl="https://api.crossref.org/works/"+doi
artinfjson=requests.get(artinfurl, headers=headers, timeout=20)  # 访问该网站
artinfdict = json.loads(artinfjson.text)
print(artinfdict["message"])
for key ,value in artinfdict["message"].items():
    print(key,value)
scihuburl="https://sci-hub.tw/"+doi
scihub_html = requests.get(scihuburl, headers=headers, timeout=20)  # 访问该网站
main_html = scihub_html.text
soup = BeautifulSoup(main_html, 'html.parser')
pdfurl=soup.find('iframe')['src']
urllib.request.urlretrieve(pdfurl, 'C:/Users/ENERGY/Desktop/download/555.pdf')
print(pdfurl)
# pdfurl = client.find_element_by_xpath("//body//iframe[1]").get_attribute('src')
# print(doi)
