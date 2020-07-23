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
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
# }
# currentPag_html = requests.get("https://sci-hub.tw", headers=headers, timeout=100)  # 访问该网站
# print(currentPag_html.status_code)

import urllib
import importlib, sys

importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def parse(DataIO, save_path):
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(DataIO)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，没有默认为空
    doc.initialize()
    # 检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages()获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接收该页面的LTPage对象
            layout = device.get_result()
            # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
            # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
            # 想要获取文本就得获取对象的text属性
            for x in layout:
                try:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        with open('%s' % (save_path), 'a') as f:
                            result = x.get_text()
                            print(result)
                            # f.write(result + "\n")
                except:
                    print("Failed")


if __name__ == '__main__':
    # 解析本地PDF文本，保存到本地TXT
    with open(r'D:/工作文件2/光散射/人体参数/Optical properties of human skin subcutaneous and mucous tissues.pdf', 'rb') as pdf_html:
        parse(pdf_html, r'D:/工作文件2/光散射/人体参数/d.txt')



