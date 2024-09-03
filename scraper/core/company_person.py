import time
from telnetlib import EC

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def chrome(headless=False):
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")

    opt.add_argument('--no-sandbox')
    opt.add_argument("--disable-extensions")
    opt.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
    opt.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함
    # opt.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

    browser = webdriver.Chrome(options=opt)
    # browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.implicitly_wait(10)
    return browser


def scraper_from_company(scape_url=None, debug=False):
    # 컴퍼니의 무한 스크롤 페이징이 끝까지 도달하게 한다.
    # 컴퍼니의 사람들의 url을 수집한다.
    # 각 사람들의 url로 이동하여 정보를 수집한다.
    # 수집한 정보를 json으로 저장하여 리턴.

    print("Hello World")

    test_url = scape_url
    if scape_url is None:
        # https://www.linkedin.com/company/dktechin/people/
        # https://www.linkedin.com/company/highspot/people/
        test_url = "https://www.linkedin.com/company/dktechin/people/"

    print("Test URL: {}".format(test_url))

    browser = chrome(headless=False)

    # 로그인
    # browser.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
    browser.set_window_position(0, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
    browser.maximize_window()

    browser.get('https://www.linkedin.com/uas/login')
    
    # 아래 예시 코드로 바꿔햐 할듯
    # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
    browser.implicitly_wait(3)

    # 로그인 정보가 담긴 파일을 읽어서 로그인
    with open("login_info.txt", "r") as f:
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()

    element_id = browser.find_element(By.ID, 'username')
    element_id.send_keys(username)

    element_id = browser.find_element(By.ID, 'password')
    element_id.send_keys(password)

    element_id.submit()

    # if url is start with https://www.linkedin.com/checkpoint
    if "checkpoint" in browser.current_url:
        print("checkpoint")

        time.sleep(10)

        # 문제풀기 보안인증으로 인해
        # 1) 그냥 문제를 푼다. headless가 아니어야함 (이거는 웹 뷰로 보여지는 것이 의미가 없어짐)
        # wait url : https://www.linkedin.com/feed/
        WebDriverWait(browser, 60).until(lambda x: x.current_url == "https://www.linkedin.com/feed/")

        # 2) headless일때 -> 자동화로 문제를 풀어야함
        # 그림 맞추는 문제 일 경우 -> 문제 제목과 이미지들을 가져와서 chat gpt?? 배보다 배꼽이 더 클 듯..
        # browser.switch_to.frame(browser.find_element(By.ID, 'captcha-internal'))
        # browser.switch_to.frame(0)
        # browser.switch_to.frame(0)
        # browser.switch_to.frame(0)
        # browser.switch_to.frame(0)
        # element_id = browser.find_element(By.ID, 'home_children_button')
        # element_id.click()  # 확인 버튼 -> 이후 문제가 나옴

    # 프로필 페이지로 이동
    # if url is start with www -> add http://
    if not test_url.startswith("http"):
        test_url = "http://" + test_url
    browser.get(test_url)
    browser.implicitly_wait(1)

    def scroll_down_page(speed=8):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            try:
                browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                new_height = browser.execute_script("return document.body.scrollHeight")
            except Exception as e:
                print("error scrolling down: {}".format(e))
                break

    scroll_down_page(8)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')



    print("End of the program")
    browser.quit()

    return None


if __name__ == '__main__':
    scraper_from_company(debug=True)
    exit(0)

