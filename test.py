import requests
from PIL import Image
from io import BytesIO
import os
import sys
from functools import reduce
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import traceback
import re
import pickle
import os
import datetime
import requests
import urllib
import json
import socket
import PyPDF2
import PyPDF4
from docx import Document
import urllib3
from googletrans import Translator
from bs4 import BeautifulSoup
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
from resumable import urlretrieve
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# urllib3.disable_warnings()
# requests.packages.urllib3.disable_warnings()
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
}

# from py_translator import Translator
# s = Translator().translate(text='Hello my friend', dest='es').text
# print(s)


# path="D:/PyCharm_GitHub_local_Repository/DataProcessMultithreading/logo.ico"
# print(os.path.basename(path))
# print("获取当前文件路径——" + os.path.realpath(path))  # 获取当前文件路径
#
# parent = os.path.dirname(os.path.realpath(path))
# print(parent)

from google_trans_new import google_translator

translator = google_translator()
translate_text = translator.translate('สวัสดีจีน', lang_tgt='en')
print(translate_text)


# if (not os.path.exists("C:/Users/ENERGY/Desktop/新建 Microsoft Visio Drawine.vsdx")):
#     print("ok")
# print("no")
# translator = Translator()
#
# # translator = Translator(service_urls=[
# #       'translate.google.cn',
# #     ])
# # str=translator.detect('이 문장은 한글로 쓰여졌습니다.', dest='zh-CN').text
# # print(str)
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
# str = translator.translate("This question already has answers here", dest='zh-CN').text
#
# print(str)