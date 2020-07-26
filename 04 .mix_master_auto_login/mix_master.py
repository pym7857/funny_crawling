from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

link = 'http://www.mixmaster.co.kr/'
driver = webdriver.Chrome('./chromedriver/chromedriver.exe')
driver.get(link)

driver.find_element_by_class_name('x2').click() # 팝업창 없애기 
sleep(2)
driver.find_element_by_name('id').send_keys('dudals98') # 아이디 '입력'
sleep(2)
driver.find_element_by_name('passwd').send_keys('jsm21kr') # 패스워드 '입력' 
sleep(2)

# 로그인 버튼 누르기 
driver.find_element_by_class_name('login_btn').click() 
sleep(2)

# 믹마 상점 버튼 누르기 
driver.find_element_by_id('snb03').click()
sleep(2)



# 웹 페이지의 소스코드를 파싱하기 위해, BeautifulSoup 를 사용
driver.get('http://www.mixmaster.co.kr/mixmall/')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 아이템 이름을 하나씩 파싱합니다.
title_list = soup.find_all('p', 'top_text')

# 모든 아이템을 출력합니다.
for title in title_list:
    print(title.text)