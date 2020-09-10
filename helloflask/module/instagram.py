from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import getpass
import time
from Modules.popupcancel import Popupcancel
from Modules.initsetting import *
import re
import os
import uiautomation as auto
import time





# email = input('인스타그램 아이디를 입력해주세요 : ')
# passward = input('인스타그램 비밀번호를 입력해주세요 : ')
#passward = getpass.getpass('인스타그램 비밀번호를 입력해주세요 : ')
email = r'donggi1012@gmail.com'
passward = r'dlehdrl1017!'

# 크롬드라이버 경로
chromedriver_path = 'C:\py_temp\chromedriver\chromedriver.exe'

# 모바일 환경세팅
# iPhone X , Pixel 2 가능
mobile_emulation = {"deviceName": "Pixel 2"}
opts = webdriver.ChromeOptions()
opts.add_experimental_option("mobileEmulation", mobile_emulation)
#opts.add_argument('headless')
opts.add_argument("--disable-gpu")


# 크롬드라이버 및 인스타그램 실행
driver = webdriver.Chrome(executable_path=chromedriver_path, options=opts)
driver.implicitly_wait(3)
instagram_url = 'https://www.instagram.com'

driver.get(instagram_url)
driver.implicitly_wait(5)


# 초기 로그인 화면 전환 버튼 클릭
driver.find_element_by_xpath('//button[contains(text(),"로그인")]').click()

# 여기선 implictly_wait 쓰면안된다. 페이지 업로드속도가 덜되는것들때문에 중간에 완료된거로 처리되서 이상하게 드라이버를 잡아버림
# 고정으로 시간을 줘야함
time.sleep(3)

input_id = driver.find_element_by_name('username')
input_pass = driver.find_element_by_name('password')



def retest(driver,arvg):
    for i in list(arvg):
        driver.send_keys(i)
        time.sleep(0.3)

retest(input_id,email)
retest(input_pass,passward)

input_pass.submit()

driver.implicitly_wait(3)

popupcancel = Popupcancel(driver)

popupcancel.popup_login()
popupcancel.popup_home()
popupcancel.scroll_down(3)
popupcancel.popup_push()

#driver.get_screenshot_as_file('screensshot.png')