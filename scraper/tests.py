import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys


def chrome(headless=False):
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(options=opt)
    browser.implicitly_wait(10)
    return browser

def scraper():
    print("Hello World")

    test_url = "https://www.linkedin.com/in/youngkwang-kim-360739244/?locale=en_US"
    print("Test URL: {}".format(test_url))

    browser = chrome(False)

    # 로그인
    browser.set_window_position(2048, 0) # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
    browser.get('https://www.linkedin.com/uas/login')
    browser.implicitly_wait(3)

    # 로그인 정보가 담긴 파일을 읽어서 로그인
    # TODO 이 부분은 UI에서 어떻게 해야할지 고민 필요
    file = open('config/login.txt') # 로그인 정보가 담긴 파일
    lines = file.readlines()
    username = lines[0]
    password = lines[1]

    elementID = browser.find_element(By.ID, 'username')
    elementID.send_keys(username)

    elementID = browser.find_element(By.ID, 'password')
    elementID.send_keys(password)

    elementID.submit()

    # 프로필 페이지로 이동
    browser.get(test_url)







    print("End of the program")




if __name__ == '__main__':
    scraper()



