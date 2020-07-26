from selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime
import pandas as pd

# review link link
link = 'https://play.google.com/store/apps/details?id=com.miso&showAllReviews=true'

# how many scrolls we need
scroll_cnt = 3

# download chrome driver (https://chromedriver.storage.googleapis.com/index.html?path=83.0.4103.39/)
driver = webdriver.Chrome('./chromedriver/chromedriver.exe')
driver.get(link)

# 결과를 저장할 디렉토리 생성
os.makedirs('result', exist_ok=True)

# (자동)스크롤을 다 해놔서 로드를 시켜놓는다.
for i in range(scroll_cnt):
    # scroll to bottom
    # execute_script: 자바스크립트를 실행한다.
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # document의 body만큼 스크롤 하게되면,
                                                                             # body 맨 밑까지 스크롤하게 됨
    time.sleep(3)

    # click 'Load more' button, if exists..
    try:
        # driver.find_element_by_xpath(): XML 문서에서 노드의 위치를 찾을 때 사용
        load_more = driver.find_element_by_xpath('//*[contains(@class,"U26fgb O0WRkf oG5Srb C0oVfc n9lfJ")]').click()
    except:
        print('Cannot find load more button..') # 더보기 버튼 없을 경우에도, 에러 나지 않도록..

# review container를 찾는다.
# jsname속성의 이름이 fk8dgd인 요소 안에 div class이름이 d15Mdf bAhLNe인 요소를 찾는다.
# find_elements 로 해야 list로 반환된다. -> find_element (X)
reviews = driver.find_elements_by_xpath('//*[@class="W4P4ne "]//div[@class="d15Mdf bAhLNe"]')

print('There are %d reviews available!' % len(reviews))
print('Writing the data..')

# create empty dataframe to store data
df = pd.DataFrame(columns=['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment'])

# get review data
for review in reviews:
    # parse string to html using bs4
    # review.get_attribute('innerHTML'): HTML요소를 텍스트(string) 형태로 가져온다음,
    # html-parser: 파싱을 한다.
    soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')  # html-parser 로 하면 오류

    # reviewer's name
    # soup.find(): 파싱된 HTML에서 요소를 찾는다
    name = soup.find(class_='X43Kjb').text  # 리뷰한 사람 이름을 긁어온다.

    # rating
    # replace('s', ''): 's'를 지운다
    # strip(): 양쪽 공백 제거
    ratings = int(soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '')
                  .replace('개를 받았습니다.', '').strip())

    # review date
    date = soup.find(class_='p2TkOb').text
    date = datetime.strptime(date, '%Y년 %m월 %d일')   # strptime: 문자열을 날짜/시간으로 변환
    date = date.strftime('%Y-%m-%d')                    # strftime: 날짜/시간을 스트링으로 변환

    # helpful
    helpful = soup.find(class_='jUL89d y92BAb').text
    if not helpful:
        helpful = 0  # 좋아요가 없을 경우 대비

    # review text
    comment = soup.find('span', jsname='fbQN7e').text
    if not comment:
        comment = soup.find('span', jsname='bN97Pc').text

    # developer comment
    developer_comment = None
    dc_div = soup.find('div', class_='LVQB0b')
    if dc_div:
        developer_comment = dc_div.text.replace('\n', ' ')

    # append to dataframe
    # df.append(): 데이터프레임에 행을 추가하여 데이터를 넣는다
    df = df.append({
        'name': name,
        'ratings': ratings,
        'date': date,
        'helpful': helpful,
        'comment': comment,
        'developer_comment': developer_comment
    }, ignore_index=True)

# finally save the dataframe into csv file
filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv(filename, encoding='utf-8-sig', index=False)  # utf-8-sig 로 해야 한글이 안깨짐

driver.stop_client() # 셀레늄 클라이언트 종료
driver.close() # 드라이버 종료

print('Done!')
