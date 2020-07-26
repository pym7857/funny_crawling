import requests
from bs4 import BeautifulSoup

# 한 주제(subject)의 대화에 대한 정보를 담는 클래스 입니다.
class Conversation:
    # 질문, 응답 두 개의 변수로 구성됩니다.
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __str__(self):
        return "질문: " + self.question + "\n답변: " + self.answer

# 모든 영어 대화 주제를 추출하는 함수 입니다.
def get_subjects():
    subjects = []

    # 전체 주제 목록을 보여주는 페이지로의 요청(request) 객체를 생성합니다.
    req = requests.get('https://basicenglishspeaking.com/daily-english-conversation-topics/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.findAll('div', {"class": "thrv_wrapper thrv_text_element tve-froala fr-box"})
    for div in divs:
        # 내부에 존재하는 <a>태그들만 추출합니다.
        links = div.findAll('a')

        # <a>태그들 내부의 텍스트를 리스트에 삽입합니다.
        for link in links:
            subjects.append(link.text)

    return subjects

subjects = get_subjects()
print('총 ', len(subjects), '개의 주제를 찾았습니다.')

i = 1

# 모든 대화 주제 각각에 접근합니다.
for sub in subjects:
    print('(', i, '/', len(subjects), ')', sub)
    req = requests.get('https://basicenglishspeaking.com/' + sub)   # 각 주제의 페이지 url
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    qnas = soup.findAll('div', {"class": "sc_player_container1"})

    for qna in qnas:
        if qnas.index(qna) % 2 == 0:
            q = qna.next_sibling    # next_sibling: (bs공식문서 : https://www.crummy.com/software/BeautifulSoup/bs4/doc/ )
                                    # q에는 질문글이 담긴다.
        else:
            a = qna.next_sibling    # a에는 답변글이 담긴다.

            # q,a 뽑은 시점에서 Coversation에 넣는다.
            c = Conversation(q, a)
            print(str(c))
            print()
    i += 1

    if i == 5:
        break