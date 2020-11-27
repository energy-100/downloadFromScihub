import os
import sys
from functools import reduce
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5 import QtCore
# import traceback
# import re
# import pickle
import os
import datetime
import requests
import urllib
import PyPDF2
import PyPDF4
from docx import Document
import urllib3
from googletrans import Translator
from bs4 import BeautifulSoup
import json
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# urllib3.disable_warnings()
# requests.packages.urllib3.disable_warnings()
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
url="https://api.crossref.org/works?query=Optical%20properties%20of%20human%20skin%20subcutaneous%20and%20mucous%20tissue"
rawdata = requests.get(url, headers=headers, timeout=10,verify=False)  # 访问该网站
data=json.loads(rawdata.text)
dataitems=data.get("message").get("items")
print(str(dataitems[0].get("title")[0]))
print(str(dataitems[0].get("author")[0]))


auth=""
for elem in dataitems[0].get("author"):
    if auth+=elem.get("given"):
        pass
    elif auth += elem["name"] + "(" + elem["sequence"] + "),"
        auth += elem["name"] + "(" + elem["sequence"] + "),"

print(auth)
print(str(dataitems[0].get("reference-count")))
print(str(dataitems[0].get("publisher")))
# print(str(dataitems[0].get("published-print").get("date-parts")[0]))
print(str(dataitems[0].get("DOI")))
print(str(dataitems[0].get("type")))
print(str(dataitems[0].get("created").get("date-time")))
print(str(dataitems[0].get("page")))
print(str(dataitems[0].get("source")))
print(str(dataitems[0].get("container-title")[0]))
print(str(dataitems[0].get("is-referenced-by-count")))
# print(str(dataitems[0].get("page").get("date-parts")))
# print(str(dataitems[0].get("page").get("date-parts")))
# print(str(dataitems[0].get("page").get("date-parts")))
# print(str(dataitems[0].get("page").get("date-parts")))
# print(str(dataitems[0].get("page").get("date-parts")))
# print(str(dataitems[0].get("published-print").get("date-parts")))
print(dataitems[0].get("created").get("date-parts")[0])
# reduce(lambda x, y: x+y , dataitems[0].get("published-print").get("date-parts"))
print(reduce(lambda x, y: str(x)+"-"+str(y), dataitems[0].get("created").get("date-parts")[0]))

import datetime
year=int(datetime.datetime.now().year)
for i in range(1950,int(datetime.datetime.now().year)+1): print(i)