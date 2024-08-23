from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def chrome(headless=False):
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")

    opt.add_argument('--no-sandbox')
    opt.add_argument("--disable-extensions")
    opt.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
    opt.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함
    opt.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

    browser = webdriver.Chrome(options=opt)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.implicitly_wait(10)
    return browser


def scraper():
    print("Hello World")

    test_url = "https://www.linkedin.com/in/suwaidaslam/"
    # test_url = "https://www.linkedin.com/in/youngkwang-kim-360739244"

    print("Test URL: {}".format(test_url))

    browser = chrome(headless=False)

    # 로그인
    # browser.set_window_position(2048, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
    browser.set_window_position(0, 0)  # 우측 세컨 모니터를 이용하기 위해 왼쪽 메인 모니터 width 만큼 이동
    browser.maximize_window()

    browser.get('https://www.linkedin.com/uas/login')
    browser.implicitly_wait(3)

    # 로그인 정보가 담긴 파일을 읽어서 로그인
    file = open('config/login.txt')  # 로그인 정보가 담긴 파일
    lines = file.readlines()
    username = lines[0]
    password = lines[1]

    element_id = browser.find_element(By.ID, 'username')
    element_id.send_keys(username)

    element_id = browser.find_element(By.ID, 'password')
    element_id.send_keys(password)

    element_id.submit()

    # 프로필 페이지로 이동
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
        location = \
            location_section.find_all('div', recursive=False)[1].find_all('div', recursive=False)[1].find_all('div',
                                                                                                              recursive=False)[
                1].find('span').get_text().strip()
        print("Location: {}".format(location))
    except Exception as e:
        print("error getting location: {}".format(e))
        location = None

    # !! 소개 섹션부터 section 태그 하위에 div id가 있는데 여기 id 명이 section 명과 같다.

    # Get about of the Person
    try:
        about_id_tag = soup.select_one("#about")
        about = about_id_tag.parent.select_one('div:nth-child(3)').get_text().strip()
        print("About: {}".format(about))
    except Exception as e:
        print("error getting about: {}".format(e))
        about = None

    # Get Experience of the Person
    try:
        experience_tag = soup.select_one("#experience")
        experience_lis = experience_tag.parent.select('div:nth-child(3) > ul > li')

        experience_list = []
        for (i, li) in enumerate(experience_lis):

            try:
                job_title_tag = li.select_one(
                    'div > div:nth-child(2) > div:nth-child(1) > div > div > div span:first-child')
                if job_title_tag is None:
                    job_title = li.select_one(
                        'div > div:nth-child(2) > div:nth-child(1) > a > div > div > div span:first-child').get_text().strip()
                else:
                    job_title = job_title_tag.get_text().strip()
            except Exception as e:
                job_title = None

            try:
                company_name_tag = li.select_one(
                    'div > div:nth-child(2) > div:nth-child(1) > div > span:nth-child(2) > span')
                if company_name_tag is None:
                    company_name = li.select_one(
                        'div > div:nth-child(2) > div:nth-child(1) > a > span:nth-child(2) > span').get_text().strip()
                else:
                    company_name = company_name_tag.get_text().strip()
            except Exception as e:
                company_name = None

            try:
                company_link = li.select('div > div:nth-child(1) a')[0]['href']
            except Exception as e:
                company_link = None

            experience_list.append({"job_title": job_title, "company_name": company_name, "company_link": company_link})

        print("Experience: {}".format(experience_list))

    except Exception as e:
        print("error getting about: {}".format(e))
        experience_list = None

    # Get Education of the Person
    try:
        education_tag = soup.select_one("#education")
        education_lis = education_tag.parent.select('div:nth-child(3) > ul > li')

        education_list = []
        for (i, li) in enumerate(education_lis):
            try:
                education_name = li.select_one(
                    'div > div:nth-child(2) > div:nth-child(1) > a > div span:first-child').get_text()
            except Exception as e:
                education_name = None

            try:
                education_period = li.select_one(
                    'div > div:nth-child(2) > div:nth-child(1) > a > span:nth-child(3) > span').get_text().strip()
            except Exception as e:
                education_period = None

            education_list.append({"name": education_name, "period": education_period})

        print("Education: {}".format(education_list))
    except Exception as e:
        print("error getting education: {}".format(e))
        education_list = None

    # make json
    # json_data = {
    #     "name": first_last_name,
    #     "location": location,
    #     "about": about,
    #     "experience": experience_list,
    #     "education": education_list
    # }

    # info.append([first_last_name, title, company_link, job_title, company_name, talksAbout, location, contacts])
    # time.sleep(5)

    print("End of the program")
    browser.quit()

    # process exit
    exit(0)


if __name__ == '__main__':
    scraper()
