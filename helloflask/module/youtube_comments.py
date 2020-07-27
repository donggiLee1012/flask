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



class Youtube:

    driverpath = os.path.join(os.path.dirname(os.getcwd()),'module','chromedriver.exe')

    s_path =os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))),'test','temps')
    now = time.localtime()
    s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


    def __init__(self,query_txt,cnt,reple_cnt):

        # 수집할 유투버명
        self.query_txt = query_txt
        # 추출할 영상수
        self.cnt = cnt
        # 추출할 댓글수
        self.reple_cnt = reple_cnt

        self.driver = webdriver.Chrome(Youtube.driverpath)

        os.makedirs(Youtube.s_path + '/' + Youtube.s + self.query_txt)

        self.ff_name = Youtube.s_path + '/' + Youtube.s + self.query_txt + '\\' + Youtube.s + '-' + self.query_txt + '.txt'
        self.fc_name = Youtube.s_path + '/' + Youtube.s + self.query_txt + '\\' + Youtube.s + '-' + self.query_txt + '.csv'
        self.fx_name = Youtube.s_path + '/' + Youtube.s + self.query_txt + '\\' + Youtube.s + '-' + self.query_txt + '.xls'



    def start(self):
        self.s_time = time.time()
        self.driver.get('https://www.youtube.com')
        time.sleep(5)
        element = self.driver.find_element_by_name("search_query")
        element.send_keys(self.query_txt)
        element.submit()
        time.sleep(2)


        if self.reple_cnt < 20:
            page_cnt = 1
        else:
            page_cnt = math.ceil(self.cnt / 20)

        if self.cnt > 20:

            i = 1
            while (i <= page_cnt):
                print("화면을 %s 회 아래로 스크롤 합니다" % i)
                Youtube.scroll_down(self.driver)
                time.sleep(1)
                i += 1

        time.sleep(2)

        html = self.driver.page_source
        soup1 = BeautifulSoup(html, 'html.parser')

        count = 0
        item = []

        print("\n")

        for i in soup1.find_all('a', 'yt-simple-endpoint style-scope ytd-video-renderer'):

            item.append(i['href'])
            count += 1

            if count == self.cnt:
                break

        print("검색된 영상 중 %s 건 동영상의 댓글을 추출하겠습니다" % self.cnt)
        print("\n")

        # 비트맵 이미지 아이콘을 위한 대체 딕셔너리를 만든다
        bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

        # 수집된 전체 URL 중에서 사용자가 입력한 수만큼의 동영상의 댓글을 수집합니다.
        # 먼저 전체 URL 을 완성 -> 동영상 페이지 열기 -> 댓글 수집 -> 다음 동영상 순으로 진행합니다
        full_url = []
        url_cnt = 0
        for x in range(0, len(item)):
            url_cnt += 1
            url = 'https://www.youtube.com/' + item[x]
            full_url.append(url)
            if url_cnt == self.cnt:
                break

        play_cnt = 1

        url2 = []
        reple2 = []
        reple3 = []
        reple4 = []
        writer2 = []
        wdate2 = []

        wb = openpyxl.Workbook()
        wb.save(self.fx_name)

        for y in range(0, len(full_url)):
            self.driver.get(full_url[y])
            time.sleep(5)
            print("\n")
            print("\n")
            print("%s 번째 동영상의 정보를 수집합니다." % play_cnt)

            i = 1
            while (i <= page_cnt):
                # print("화면을 %s 회 아래로 스크롤 합니다" %i)
                Youtube.scroll_down(self.driver)
                time.sleep(5)
                i += 1

            html = self.driver.page_source
            soup2 = BeautifulSoup(html, 'html.parser')

            t_count_0 = soup2.select('#count')
            t_count_1 = t_count_0[1].get_text()
            t_count_2 = t_count_1.replace(",", "")
            t_count_3 = re.search("\d+", t_count_2)
            t_count_4 = int(t_count_3.group())

            t_title_1 = soup2.select('#info-contents')
            t_title_2 = t_title_1[0].find('h1').get_text()
            t_title_3 = t_title_2.translate(bmp_map).replace("\n", "")

            t_view_1 = soup2.find('yt-formatted-string',
                                  'count-text style-scope ytd-comments-header-renderer').get_text()  # .get_text( ).replace("\n","")
            t_view_2 = t_view_1.replace(",", "")
            t_view_3 = re.search("\d+", t_view_2)
            print(t_view_1)
            t_view_4 = int(t_view_3.group())

            print("=" * 80)
            print("%s 번째 동영상의 조회수는 %s 회 이고 수집할 댓글은 총 %s개 입니다" % (play_cnt, t_count_4, t_view_4))
            print("%s 번째 동영상의 제목은 %s 입니다" % (play_cnt, t_title_3))
            print("=" * 80)
            print("\n")
            print("%s 번째 동영상에서 댓글 수집을 시작합니다" % play_cnt)
            print("댓글의 개수가 많아서 시간이 걸릴 수 있으니 잠시 기다려 주세요~~^^")
            print("\n")

            # Step 5. 화면을 스크롤해서 아래로 이동합니다

            # page_cnt = math.ceil(t_view_4 / 19)

            i = 1
            while (i <= page_cnt + 1):
                print("%s 번째 페이지의 댓글을 수집하는 중입니다~" % i)
                Youtube.scroll_down(self.driver)
                time.sleep(0.5)
                i += 1

            # Step 6. 내용을 수집합니다

            time.sleep(2)

            html = self.driver.page_source
            soup3 = BeautifulSoup(html, 'html.parser')

            count = 0
            d2 = 0

            reple_result = soup3.select('#comments > #sections > #contents')

            for a in range(0, self.reple_cnt + 1):
                count += 1

                f = open(self.ff_name, 'a', encoding='UTF-8')
                f.write("\n")
                f.write("------------------------------------------------------------------" + "\n")

                # 댓글 작성자
                try:
                    writer = reple_result[0].select("#header-author > #author-text")[a].get_text().replace("\n",
                                                                                                           "").strip()
                except IndexError:
                    break
                else:
                    print("\n")
                    print("%s 번째 영상의 %s 번째  댓글 " % (play_cnt, count))
                    print("-" * 70)

                    # 유튜브 URL 주소
                    print("1.URL 주소:", full_url[y])
                    f.write("1.유투브 URL주소: " + full_url[y] + "\n")
                    url2.append(full_url[y])

                    print("2.댓글 작성자명:", writer)
                    f.write("2.댓글 작성자명: " + writer + "\n")
                    writer2.append(writer)

                    # 댓글 작성일자
                    wdate = reple_result[0].select("yt-formatted-string.published-time-text > a.yt-simple-endpoint")[
                        a].get_text().replace("\n", "")

                    print("3.댓글 작성일자:", wdate)
                    f.write("3.댓글 작성일자: " + wdate + "\n")
                    wdate2.append(wdate)

                    # 댓글 내용
                    reple1 = reple_result[0].select('#expander > #content > #content-text')[a].get_text().replace("\n",
                                                                                                                  "")

                    reple2 = reple1.translate(bmp_map).replace("\n", "")
                    print("4.댓글 내용:", reple2)
                    f.write("4.댓글 내용: " + reple2 + "\n")
                    reple3.append(reple2)

                f.close()

                if count == self.reple_cnt:
                    break

            time.sleep(2)
            play_cnt += 1

        return url2,writer2,wdate2,reple3,count

    def save(self,url2,writer2,wdate2,reple3,count):

        youtube_reple = pd.DataFrame()
        youtube_reple['URL 주소'] = url2
        youtube_reple['댓글작성자명'] = pd.Series(writer2)
        youtube_reple['댓글작성일자'] = pd.Series(wdate2)
        youtube_reple['댓글 내용'] = pd.Series(reple3)

        # csv 형태로 저장하기
        youtube_reple.to_csv(self.fc_name, encoding="utf-8-sig", index=True)

        # 엑셀 형태로 저장하기
        youtube_reple.to_excel(self.fx_name, index=True)

        e_time = time.time()
        t_time = e_time - self.s_time

        # txt 파일에 크롤링 요약 정보 저장하기
        orig_stdout = sys.stdout
        f = open(self.ff_name, 'a', encoding='UTF-8')
        sys.stdout = f

        print("\n")
        print("=" * 50)
        print("총 소요시간은 %s 초 이며," % t_time)
        print("총 저장 건수는 %s 건 입니다 " % count)
        print("=" * 50)

        sys.stdout = orig_stdout
        f.close()

        print("\n")
        print("=" * 100)
        print("1.요청된 총 %s 건 동영상 리뷰 중에서 실제 크롤링 된 리뷰수는 %s 건입니다" % (self.cnt, count))
        print("2.총 소요시간은 %s 초 입니다 " % round(t_time, 1))
        print("3.파일 저장 완료: txt 파일명 : %s " % self.ff_name)
        print("4.파일 저장 완료: csv 파일명 : %s " % self.fc_name)
        print("5.파일 저장 완료: xls 파일명 : %s " % self.fx_name)
        print("=" * 100)

        time.sleep(3)

        self.driver.close()

    def scroll_down(driver):
        # driver.execute_script("window.scrollTo(500,document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0,3000);")  # 한페이지 20개씩 출력값
        time.sleep(5)
