import random
import time
from pyquery import PyQuery as pq
import requests
from bs4 import BeautifulSoup
import math
import os
import sys
import random
from selenium.webdriver.common.action_chains import ActionChains
import operator
from ping3 import ping
from selenium import webdriver
import urllib
import socket
def ping_host(ip):
    """
    获取节点的延迟的作用
    :param node:
    :return:
    """
    ip_address = ip
    response = ping(ip_address)
    print(response)
    delay=-1
    if response is not None:
        delay = int(response * 1000)
        return delay
        # print(delay, "延迟")
        # # 下面两行新增的
    return delay

'''请求头'''
headers = {
    "Connection": "Close",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    # "Cookie": "BIDUPSID=10FA6916F18B54FF38D559EADD614CF7; PSTM=1559717595; HMACCOUNT=1A654E98409FD986; BDUSS=NQUWFOU2piQmRvUjZ-alQyWHFFMGhYQlJWUGlzNm95Z2J5SXNySnhVbFBaUmhlRUFBQUFBJCQAAAAAAAAAAAEAAADZUV0hv7S6o7XE0MTH6TE5OTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE~Y8F1P2PBdZn; MCITY=-%3A; BAIDUID=8FE77A473BC7AD385A938DB0BD9CD39F:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=CFAOJeC62wIBEoJuuOfyUIOrkEpgL5bTH6aoRvqxCFQrpapl1wQ1EG0PHU8g0KAbpgWlogKKBmOTHn_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tb4D_CIyfII3fP36q46EbnL_hxJb54cQ24o2WbCQQbIW8pcNLTDKhtAlqq5X-RQ9MIQPal7-2hPhOl7C-lO1j4_eyHQHhRJeb66K2lRPfP3Jfh5jDh3o3jksD-Rt5foRHR5y0hvc0J6cShnkBUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2b6QhDGAJtTkqJJPsBTrL2nTVHtoG-tT8Mt_Hqxby26nm3e69aJ5nJDobOqoHhU6h5f4E2JoAWbjW36RM2I5tQpP-HJ7-5RQWLUKuKl3KbPADbaCDKl0MLpnlbb0xyUQDK--ihMnMBMnGamOnanr73fAKftnOM46JehL3346-35543bRTLnLy5KJYMDcnK4-Xj5v-eH3P; delPer=0; PSINO=1; HMVT=6bcd52f51e9b3dce32bec4a3997715ac|1586651518|; H_PS_PSSID=1434_31170_21107_30826_31186_30905_31270_30824_31085_31163_31195",
    # "Host": "hm.baidu.com",
    # "Referer": "https://blog.csdn.net/dreamzuora/article/details/89931656",


}

'''代理ip'''
proxies = {
    "http": "http://202.121.96.33:8086",
    "http": "http://58.253.154.179:9999",
    "http": "http://163.204.243.51:9999",
    "http": "http://183.166.20.179:9999",
    "http": "http://183.166.20.179:9999",

    # "https": "https://221.228.17.172:8181",

}

def testurlable():

    urls=[
        "https://sci-hub.tw/",
        "https://sci-hub.hk/",
        "https://sci-hub.tw",
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
    ableurls=[]

    for i in range(len(urls)):
        try:
            currentPag_html = requests.get(urls[i], headers=headers, proxies=proxies)  # 访问该网站
        except Exception:
            print(urls[i] + "失败！")
            continue
        # 先判断是否成功访问
        if currentPag_html.status_code == 200:
            print(urls[i]+"成功！")
            # delay=ping_host(urls[i])
            # print(urls[i]+"成功！ 延迟：",delay)
            ableurls.append(urls[i])
        else:
            print(urls[i]+"失败！")


def getart():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory":"C:/Users/ENERGY/Desktop/download", "download.prompt_for_download":False, }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--auto-open-devtools-for-tabs");
    chrome_options.add_argument(
        "user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36")
    client = webdriver.Chrome(chrome_options=chrome_options)
    # 如果没有把chromedriver加入到PATH中,就需要指明路径 executable_path='/home/chromedriver'

    client.get("https://sci-hub.tw/")
    # time.sleep(5)
    client.find_element_by_xpath("//input[@name='request']").send_keys("Quantum mechanics and hidden variables: A test of Bell's inequality by the measurement of the spin correlation in low-energy proton-proton scattering")
    # time.sleep(1)
    client.find_element_by_xpath("//div[@id='open']").click()
    # time.sleep(3)
    pdfurl=client.find_element_by_xpath("//body//iframe[1]").get_attribute('src')
    urllib.request.urlretrieve(pdfurl, 'C:/Users/ENERGY/Desktop/download/1.pdf')
    # client.find_element_by_xpath("//a[@href = '#']").click()
    # sizeDict = client.get_window_size()
    # button = client.find_element_by_class_name("nc_iconfont.btn_slide")
    # action = ActionChains(client)
    # action.click_and_hold(button).perform()
    # action.reset_actions()
    # action.move_by_offset(280, 0).release().perform()
    # action.click_and_hold()
    time.sleep(30)
    # 关闭谷歌浏览器

    # client.get("https://blog.csdn.net/lch551218/article/details/103805042")

    content = client.page_source
    # client.close()
    print(content)
    # client.quit()


# testurlable()
getart()
# urllib.request.urlretrieve("https://cyber.sci-hub.tw/MTAuMTEwMy9waHlzcmV2ZC4xNC4yNTQz/lamehi-rachti1976.pdf#view=FitH",'D:/1.pdf')