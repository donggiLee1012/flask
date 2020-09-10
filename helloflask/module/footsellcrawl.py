import math

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import re
import numpy as np
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os,sys

class Footsell:


    robots = 'robots.txt'
    footsell = 'https://footsell.com'
    f_uri = r'/g2/bbs/board.php?bo_table=m51&r=ok'
    # request로 driver 없는거로 바꿔주자
    driverpath = r'C:\Users\donggi\Desktop\python_flask\helloflask\module\chromedriver.exe'
    time_marker = time.strftime('%Y-%m-%d', time.localtime())


    def __init__(self,query_txt,size,many):



        self.homepath = os.path.expanduser('~')

        s_path = os.path.join(self.homepath, 'Desktop', 'footsell_marketprice')
        self.now = time.localtime()
        self.s = '%04d-%02d-%02d-%02d-%02d' % (self.now.tm_year, self.now.tm_mon, self.now.tm_mday,
                                               self.now.tm_hour, self.now.tm_min)
        self.query_txt = query_txt

        self.size = int(size)
        self.many = int(many)

        if os.path.exists(s_path + '/' + self.s + query_txt):
            pass
        else:
            os.makedirs(s_path + '/' + self.s + query_txt)

        self.ff_name = s_path + '/' + self.s + self.query_txt + '\\' + self.s + '-' + self.query_txt + '.txt'
        self.fc_name = s_path + '/' + self.s + self.query_txt + '\\' + self.s + '-' + self.query_txt + '.csv'
        self.fx_name = s_path + '/' + self.s + self.query_txt + '\\' + self.s + '-' + self.query_txt + '.xls'

        # options = Options()
        # options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        # options.add_argument("disable-gpu")
        # options.add_argument("lang=ko_KR")
        # self.driver = webdriver.Chrome(self.driverpath, options=options)
        self.driver = webdriver.Chrome(Footsell.driverpath)

        self.driver.implicitly_wait(10)
        self.driver.get(Footsell.footsell + Footsell.f_uri)


    def search(self):
        # 검색
        search_box = self.driver.find_element_by_css_selector('#list_search_text_input')
        search_box.send_keys(self.query_txt)
        search_box.send_keys(Keys.ENTER)

        # 사이즈별 선택한게있으면 실행
        if self.size !='':
            input_size = 'option[value="' + '{}"]'.format(self.size)
            size_select = self.driver.find_element(By.CSS_SELECTOR, input_size)
            size_select.click()


    def parser(self,soup_list=[]):

        for j in range(math.ceil(int(self.many) / 40)):
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(2)
            border_list = soup.find_all(id=re.compile('list_row_'))

            if border_list == []:
                print('검색결과없음')
                break

            soup_list.append(border_list)

            try:
                self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[j].send_keys(Keys.ENTER)
            except:
                break

    def check(self,border_list_att):
        # 제목
        try:
            title = border_list_att.find('span', id=re.compile('^list_subject_')).text.strip()

        except:
            title = border_list_att.find('span', class_='smallfont color_aaa').text.strip()

        # 컨디션
        condition = border_list_att.find('span', class_='list_market_used han').text

        # 사이즈
        size = border_list_att.find('span', class_='list_market_size').text

        # 가격
        try:
            price = border_list_att.find('div', class_=re.compile('^list_market_price')).text.strip()
        except:
            price = border_list_att.find('span', class_='color_aaa normal smallfont').text.strip()

        # 판매자명
        seller = border_list_att.find('div', class_=re.compile('^float_left list_market_name')).text.strip()

        # 업로드 시각
        uploadtime = border_list_att.find('span', class_='list_table_dates').text.strip()

        # uri
        uri = border_list_att.find('a').get('href')

        # img
        img = border_list_att.find('img').get('src')

        if ':' in uploadtime:
            uploadtime = Footsell.time_marker

        return [title, condition, size, price, seller, uploadtime, uri, img]


