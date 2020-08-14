# url
# youtuber
# name
# comments
# like
#
# youtube 댓글수집 프로세스 모듈화한뒤
# 위에 5개의 변수 init.py에서 값을 받을수있게해야함
# 그뒤 youtube.html 에 뿌려준다.


# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import re
import math
import numpy
import pandas as pd
import xlwt
import random
import os
import openpyxl
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


class Youtube:

    def __init__(self, query_txt, cnt, reple_cnt):

        #self.driverpath = os.path.join(os.path.dirname(os.getcwd()), 'module', 'chromedriver.exe')

        self.driverpath =r'C:\Users\donggi\Desktop\python_flask\helloflask\module\chromedriver.exe'

        self.homepath = os.path.expanduser('~')

        s_path = os.path.join(self.homepath, 'Desktop', 'youtube_comments')
        self.now = time.localtime()
        self.s = '%04d-%02d-%02d-%02d-%02d' % (self.now.tm_year, self.now.tm_mon, self.now.tm_mday,
                                               self.now.tm_hour, self.now.tm_min)
        self.query_txt = query_txt
        self.cnt = int(cnt)
        self.reple_cnt = int(reple_cnt)

        if os.path.exists(s_path + '/' + self.s + query_txt):
            pass
        else:
            os.makedirs(s_path + '/' + self.s + query_txt)

        self.ff_name = s_path + '/' + self.s + self.query_txt + '\\' + self.s + '-' + self.query_txt + '.txt'
        self.fc_name = s_path + '/' + self.s + self.query_txt + '\\' + self.s + '-' + self.query_txt + '.csv'
        self.fx_name = s_path + '/' + self.s + self.query_txt + '\\' + self.s + '-' + self.query_txt + '.xls'

        options = Options()
        #         ua = UserAgent(verify_ssl=False)
        #         userAgent = ua.random
        #         print(userAgent)
        #         options.add_argument(f'user-agent={userAgent}')
        # options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        # options.add_argument("disable-gpu")
        # options.add_argument("lang=ko_KR")
        #self.driver = webdriver.Chrome(self.driverpath, options=options)
        self.driver = webdriver.Chrome(self.driverpath)
        self.driver.get('https://www.youtube.com')

    def scroll_down(driver, num, sleepnum=5):
        # driver.execute_script("window.scrollTo(500,document.body.scrollHeight);")
        for i in range(num):
            driver.execute_script("window.scrollBy(0,6000);")  # 한페이지 20개씩 출력값
            time.sleep(sleepnum)

    def search(self, thumbnail):
        time.sleep(3)
        element = self.driver.find_element_by_name('search_query')
        element.send_keys(self.query_txt)
        element.submit()
        time.sleep(2)

        if self.reple_cnt < 20:
            self.r_cnt = 1
        else:
            self.r_cnt = math.ceil(self.reple_cnt / 20)

        if self.cnt < 20:
            c_cnt = 1
        else:
            c_cnt = math.ceil(self.cnt / 20)
            Youtube.scroll_down(self.driver, c_cnt)

        Youtube.scroll_down(self.driver, c_cnt)

        contents = []

        count = 0

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')  # 검색결과 유튜브 페이지 soup

        for j in range(self.cnt):
            thumbnail.append(soup.select('#contents #dismissable #thumbnail > yt-img-shadow > #img')[j]['src'])

        for i in soup.find_all('a', 'yt-simple-endpoint style-scope ytd-video-renderer'):
            contents.append('https://www.youtube.com/' + i['href'])
            count += 1
            if count == self.cnt:
                break
        # contents =[ 유튜브 검색결과 링크들 ]

        # Youtube.utuber_parser(contents)
        return contents

    def utuber_parser(self, href, pool):
        self.driver.implicitly_wait(10)
        self.driver.get(href)
        time.sleep(3)
        Youtube.scroll_down(self.driver, self.r_cnt, 7)

        self.driver.implicitly_wait(10)
        html = self.driver.page_source
        soup1 = BeautifulSoup(html, 'html.parser')

        # 총 댓글수

        comment = soup1.select('#count > yt-formatted-string')[0].get_text()

        comment1 = comment.replace(",", "")
        comment2 = int(re.search('\d+', comment1).group())

        # 영상 제목
        title = soup1.select('#container > h1 > yt-formatted-string')[0].get_text()

        # 조회수
        view = soup1.select('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer')[
            0].get_text()
        view1 = view.replace(",", "")
        view2 = int(re.search('\d+', view1).group())

        # 유투버명
        youtuber = soup1.select('#upload-info #text')[0].get_text()

        # 구독자수
        try:
            sub = soup1.select('#owner-sub-count')[0].get_text()
            sub1 = re.search('\d+.*', sub).group().strip()
        except:
            sub1 = '비공개'

        # 게시날짜
        up_date = soup1.select('#date > yt-formatted-string')[0].get_text()
        up_date1 = up_date.replace(" ", "")

        # 좋아요 수
        like = soup1.select('#top-level-buttons > ytd-toggle-button-renderer:nth-child(1) > a #text')[0].get_text()

        # 싫어요 수
        dislike = soup1.select('#top-level-buttons > ytd-toggle-button-renderer:nth-child(2) > a #text')[
            0].get_text()

        pool_list = []
        pool_list.append(title)
        pool_list.append(view2)
        pool_list.append(up_date1)
        pool_list.append(like)
        pool_list.append(dislike)
        pool_list.append(sub1)
        pool_list.append(comment2)
        pool_list.append(youtuber)

        pool.append(pool_list)

        return soup1

    def comment_parser(self, soup1):

        comment_list = []

        current_reple_cnt = len(soup1.select('#comments #sections #contents #comment'))
        check = self.reple_cnt

        # 댓글 추출 갯수 조정
        if check > current_reple_cnt:
            check = current_reple_cnt

        count = 0
        print('start...')
        for k in range(check):
            c_pool = []

            name_s = soup1.select('#author-text')[k].get_text().strip()
            source_s = soup1.select('#content-text')[k].get_text()
            rdate_s = soup1.select('#header-author > yt-formatted-string > a')[1].get_text()
            rdate_s1 = re.search('.*전', rdate_s).group()
            like_s = soup1.select('#vote-count-middle')[k].get_text().strip()
            youtuber_s = soup1.select('#upload-info #text')[0].get_text()

            with open(self.ff_name, 'a', encoding='UTF-8') as f:
                f.write("------------------------------------------------------------------" + "\n")
                f.write("\n***** {} 번째  댓글 *****\n".format(count + 1))
                f.write("1.유튜버 : " + youtuber_s + "\n")
                f.write("2.댓글 작성자 : " + name_s + "\n")
                f.write("3.댓글 내용 : " + source_s + "\n")
                f.write("4.댓글 좋아요수 : " + like_s + "\n")
                f.write("5.댓글 게시일 : " + rdate_s1 + "\n\n")
            count += 1

            # 작성자 name
            c_pool.append(name_s)

            # 댓글 원문
            c_pool.append(source_s)

            # 댓글 좋아요수
            c_pool.append(like_s)

            # 유튜버
            c_pool.append(youtuber_s)

            # 댓글 게시일
            c_pool.append(rdate_s1)

            comment_list.append(c_pool)

        return comment_list