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

    test_url = "https://www.linkedin.com/in/suwaidaslam/"
    print("Test URL: {}".format(test_url))

    browser = chrome(False)

    # 로그인
    browser.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
    browser.maximize_window()

    browser.get('https://www.linkedin.com/uas/login')
    browser.implicitly_wait(3)

    # 로그인 정보가 담긴 파일을 읽어서 로그인
    # TODO 이 부분은 UI에서 어떻게 해야할지 고민 필요
    file = open('config/login.txt')  # 로그인 정보가 담긴 파일
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
    browser.implicitly_wait(1)

    def scroll_down_page(speed=8):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = browser.execute_script("return document.body.scrollHeight")

    scroll_down_page(speed=8)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    # profile image url
    try:
        profile_img = soup.select('section.artdeco-card')[0].select('img')[1]['src']
        print("profile image url: {}".format(profile_img))
    except Exception as e:
        print("error getting profile image url: {}".format(e))
        profile = None

    # Get Name of the person
    try:
        first_last_name = soup.select('section.artdeco-card')[0].select('h1')[0].get_text().strip()
        print("Name: {}".format(first_last_name))
    except Exception as e:
        print("error getting name: {}".format(e))
        first_last_name = None

    # Get Location of the Person
    try:
        location_section = soup.findAll('section', {'class': 'artdeco-card'})[0]
        location = location_section.find_all('div', recursive=False)[1].find_all('div', recursive=False)[1].find_all('div',recursive=False)[1].find('span').get_text().strip()
        print("Location: {}".format(location))
    except Exception as e:
        print("error getting location: {}".format(e))
        location = None

    # TODO 소개 섹션부터 section 태그 하위에 div id가 있는데 여기 id 명이 section 명과 같다.

    #
    # # Get Title of the Person
    # try:
    #     title = name_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
    # except:
    #     title = None
    #
    # # Get Company Link of the Person
    # try:
    #     exp_section = soup.find('section', {'id': 'experience-section'})
    #     exp_section = exp_section.find('ul')
    #     li_tags = exp_section.find('div')
    #     a_tags = li_tags.find('a')
    #
    #     company_link = a_tags['href']
    #     company_link = 'https://www.linkedin.com/' + company_link
    # except:
    #     company_link = None
    #
    # # Get Job Title of the Person
    # try:
    #     job_title = li_tags.find('h3', {'class': 't-16 t-black t-bold'}).get_text().strip()
    # except:
    #     job_title = None
    #
    # # Get Company Name of the Person
    # try:
    #     company_name = li_tags.find('p',
    #                                 {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).get_text().strip()
    # except:
    #     company_name = None
    #
    # contact_page = test_url + 'detail/contact-info/'
    # browser.get(contact_page)
    # browser.implicitly_wait(1)
    #
    # contact_card = browser.page_source
    # contact_page = BeautifulSoup(contact_card, 'lxml')
    # # Get Linkdin Profile Link and Contact details of the Person
    # try:
    #     contact_details = contact_page.find('section', {
    #         'class': 'pv-profile-section pv-contact-info artdeco-container-card ember-view'})
    #     contacts = []
    #     for a in contact_details.find_all('a', href=True):
    #         contacts.append(a['href'])
    # except:
    #     contacts.append('')
    # info.append([first_last_name, title, company_link, job_title, company_name, talksAbout, location, contacts])
    # time.sleep(5)

    print("End of the program")
    browser.quit()


if __name__ == '__main__':
    scraper()
