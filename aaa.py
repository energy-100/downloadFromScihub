from googletrans import Translator
import requests
import numpy as np
from ping3 import ping
from selenium import webdriver
import urllib
from bs4 import BeautifulSoup
#
# translator = Translator()
# data=translator.translate('안녕하세요.')
# html=requests.post("https://sci-hub.tw",{"request": "Spin Correlation Measurement in Proton-Proton Scattering and Comparison with the Theories of the Local Hidden Variables"})
# print(html.status_code)
# main_html = html.text
# soup = BeautifulSoup(main_html, 'html.parser')
# identifyingcode=soup.find_all('captcha')
# print(len(identifyingcode))
# pdfurl = soup.find('iframe')['src']
# print(pdfurl)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
currentPag_html = requests.get("https://sci-hub.tw", headers=headers, timeout=100)  # 访问该网站
print(currentPag_html.status_code)


