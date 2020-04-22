
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
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

url="https://api.serpwow.com/live/search?api_key=E744D836229E40FBA56CDA94138DBB39&q=pizza"
# url="https://mc.yandex.ru/watch/10183018?page-url=https%3A%2F%2Fsci-hub.tw%2F10.1103%2Fphysrevd.14.2543&charset=utf-8&force-urlencoded=1&browser-info=ti%3A1%3Adp%3A0%3Ans%3A1587134670271%3As%3A1920x1080x24%3Ask%3A1.25%3Aadb%3A2%3Afpr%3A67501995301%3Acn%3A1%3Aw%3A688x742%3Az%3A480%3Ai%3A20200417224448%3Aet%3A1587134688%3Aen%3Autf-8%3Ac%3A1%3Ala%3Azh-cn%3Aar%3A1%3Anb%3A1%3Acl%3A1153%3Als%3A861413449210%3Arqn%3A47%3Arn%3A495509948%3Ahid%3A359903306%3Ads%3A%2C%2C%2C%2C%2C%2C%2C%2C%2C3279%2C3279%2C0%2C%3Agdpr%3A14%3Afu%3A1%3Av%3A1850%3Arqnl%3A1%3Ast%3A1587134688%3Au%3A157542004773320639%3App%3A3629563401"
f=currentPag_html = requests.post(url)  # 访问该网站
# with open("aa.gif", 'wb') as ff:
#     ff.write(f)
print(currentPag_html.status_code)
print(currentPag_html.text)
