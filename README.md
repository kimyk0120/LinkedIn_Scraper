# LinkedIn Profile Scraper 

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![pythonbadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

This project is a web application that scrapes LinkedIn profiles that provide public information. 


--> intro image here



This scraper will extract publicly available data: 

**🧑‍🎨 Profile:** ......name, talks about, title, location, and url

**👨‍💼 Experiences:** ....job title, company name and job type and, company url

**🗺️ Contact:** ... Email and Website Link

## Stacks
```angular2html
Django 5.0.7
Python 3.10.11
tailwindcss 3.0.0
```

## Prerequisites
- make config/login.txt file in scaper directory and write your linkedin email and password
```angular2html
your_email  # first line your_email
your_password  # second line your_password
```
  
## How to Run 

- Clone the repository
- Install Requirements
```bash
$ pip install -r requirements.txt
```
-  Run Django Server
```bash
$ python manage.py runserver
```

- Tailwind Build (for development)
```bash
$ npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```

---

## DONE
- 프로젝트 init 
- django 프로젝트 생성 및 기초 설정
- tailwindcss 설정
- 인덱스 페이지 디자인


## TODO
- 코어 로직 구현


## Trouble Shooting
- https://velog.io/@awo3sr/TIL-17-%ED%8C%8C%EC%9D%B4%EC%B0%B8-x-windows-949-%EC%98%A4%EB%A5%98

## Contact

For any feedback or queries, please reach out to me at [kimyk0120@gmail.com](kimyk0120@gmail.com).

