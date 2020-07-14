from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import re
import numpy as np
import pandas as pd
import time
from selenium.webdriver.common.by import By
from konlpy.tag import Hannanum,Kkma,Okt,Komoran
import os,sys

print(os.getcwd())

class Footsell:
    robots = 'robots.txt'
    footsell = 'https://footsell.com/'
    f_uri = 'g2/bbs/board.php?bo_table=m51&r=ok'
    # request로 driver 없는거로 바꿔주자
    driverpath = r'C:\Users\guide\Desktop\mulitdong\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(Footsell.driverpath)
        self.df = pd.DataFrame(columns=['title', 'size', 'condition', 'price', 'days', 'seller', 'site'])
        self.search = ''


    def check(border_list_att, time_marker):
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
            uploadtime = time_marker

        return [title, condition, size, price, seller, uploadtime, uri, img]


    def start(self, search):
        self.driver.get(Footsell.footsell + Footsell.f_uri)
        self.driver.implicitly_wait(3)

        search_box = self.driver.find_element_by_css_selector('#list_search_text_input')

        self.search = search
        if self.search == '':
            pass
        else:
            search_box.send_keys(self.search)
            search_box.send_keys(Keys.ENTER)

    def parser(self):
        pool_list = []
        time_marker = time.strftime('%Y-%m-%d', time.localtime())

        page = self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')

        if len(page) > 10:
            for i in range(len(page) - 1):
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                time.sleep(2)
                border_list = soup.find_all(id=re.compile('list_row_'))

                if self.search == "":

                    # 검색값없으면
                    border_list = border_list[3:]
                else:
                    pass

                for j in border_list:
                    pool_list.append(Footsell.check(j, time_marker))

                self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[i].send_keys(Keys.ENTER)
                time.sleep(3)

        elif len(page) <= 10:
            for i in range(len(page)):
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                time.sleep(2)
                border_list = soup.find_all(id=re.compile('list_row_'))

                for j in border_list:
                    pool_list.append(Footsell.check(j, time_marker))

                self.driver.find_elements(By.CSS_SELECTOR, 'ul>li>a')[i].send_keys(Keys.ENTER)
                time.sleep(3)

        else:
            print('Error')

        return pool_list