from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
from PIL import Image
from konlpy.tag import Kkma
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
kkma = Kkma()

from matplotlib import font_manager, rc
font_path = 'C:/Users/(글꼴 경로 설정)/NanumGothic.ttf'  # 글꼴 경로 설정
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

from wordcloud import WordCloud

import pyautogui
url = pyautogui.prompt(title="DaangnCrawling-TIL", text="당근마켓 계정 주소를 입력하세요\n\n# 틀린 주소 예 : https://www.daangn.com/u/상세주소?install_from=user_profile\n# 맞는 주소 예 : https://www.daangn.com/u/상세주소")

kkma_details = "" # 자연어 처리 후 코드

import sys, os
if  getattr(sys, 'frozen', False): 
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path) # 실행 안될 시 새로운 chromedriver 버전으로 변경
else:
    driver = webdriver.Chrome()

driver.get(url)
time.sleep(3)

# 유저 닉네임 추출(엑셀 파일 생성에 사용)
user = driver.find_element_by_id("nickname").text
user = user.split(' ', 1)[0]
region_name = driver.find_element_by_id("region_name").text

# 판매 물품 개수 파악
SCROLL_PAUSE_SEC = 2

last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_SEC)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 판매 갯수 추출
img = driver.find_elements_by_tag_name("img")
img_nums = len(img) - 9

# y 는 section[숫자], z는 article[숫자]
y = int(img_nums / 18)
z = int(img_nums % 18)
if img_nums % 18 == 0:
    y = y - 1

data = []  # 크롤링한 데이터를 [제목, 본문] 형식으로 저장할 딕셔너리
data.append([user, region_name])

# 숨김 처리된 글 탐지용
hide_article = False

# 현재 페이지 수
current_num = 1

# 카테고리(item_category) 변수
life = 0  # 생활용품
child = 0  # 유아동
female = 0  # 여성의류/잡화
male = 0  # 남성의류/잡화
interest = 0  # 취미/여가
beauty = 0  # 뷰티/미용
pet = 0  # 반려동물용품
etc = 0  # 기타

life_list = ["생활가전", "가구/인테리어"]
child_list = ["유아도서", "유아동"]
female_list = ["여성잡화", "여성의류"]
male_list = ["남성패션/잡화"]
interest_list = ["게임/취미", "스포츠/레저", "도서/티켓/음반", "식물"]
beauty_list = ["뷰티/미용"]
pet_list = ["반려동물용품"]
etc_list = ["기타 중고물품", "삽니다", "디지털기기"]

# 디테일(detail) 변수
strings = []

for n in range(1, y + 2):
    new_link = str(url) + '?page=' + str(n)
    driver.get(new_link)

    for m in range(1, 19): 

        driver.find_element_by_xpath(
            '//*[@id="user-records"]/section/article[{0}]/a/div[1]/img'.format(m)).click()
        time.sleep(2)

        try:
            hide_article = driver.find_element_by_id("no-article").text
        except:
            pass

        if hide_article != 0:
            m = m + 1
            print("현재 상품 : {0} / 총 상품 개수 : {1}\n-----------------------------------".format(current_num, img_nums))
            current_num = current_num + 1
            hide_article = False
        else:
            item_titles = driver.find_element_by_id("article-title").text
            item_category = driver.find_element_by_id("article-category").text
            item_category = item_category.split(' ', 1)[0]
            item_details = driver.find_elements_by_id("article-detail")
            item_links = driver.current_url

            for i in item_details:
                i = i.text
            detail = "".join(i)

            if n == 1 and m == 1:
                list1 = [user, region_name, item_titles, item_category, detail]

            else:
                list1 = list1 = ['', '', item_titles, item_category, detail]

                if item_category in life_list:
                    life += 1
                elif item_category in child_list:
                    child += 1
                elif item_category in female_list:
                    female += 1
                elif item_category in male_list:
                    male += 1
                elif item_category in interest_list:
                    interest += 1
                elif item_category in beauty_list:
                    beauty += 1
                elif item_category in pet_list:
                    pet += 1
                elif item_category in etc_list:
                    etc += 1

            # 개인정보 中 전화번호 탐지
            strings = detail.split()
            if "***-****-****" in strings:
                print('개인정보 중 전화번호가 존재합니다.')

            # 불용어 처리
            kkma_details = kkma_details + ' '.join(kkma.nouns(detail))

            stop_words = []
            f = open('./stopwords.txt', 'r', encoding = 'utf-8')

            lines = f.readlines()
            for line in lines:
                line = line.strip()
                stop_words.append(line)
            f.close()

            word_tokens = word_tokenize(kkma_details)
            
            word_result = [w for w in word_tokens if w not in stop_words]
            word_result = ' '.join(word_result)

            wordcloud = WordCloud(width=500, height=500, margin=0, background_color='white',
                                    font_path = './NanumGothic.ttf').generate(word_result)

            data.append(list1)
            print("현재 상품 : {0} / 총 상품 개수 : {1}\n-----------------------------------".format(current_num, img_nums))
            
            current_num = current_num + 1

        if current_num > img_nums:
            break
        driver.back()

# 카테고리 시각화
x = ['생활용품', '유아동', '여성의류/잡화', '남성의류/잡화', '취미/여가', '뷰티/미용', '반려동물용품', '기타']
y = [life, child, female, male, interest, beauty, pet, etc]
title = '{0}_카테고리 시각화'.format(user)
pyplot.title(title)
pyplot.ylabel('개수')
pyplot.xticks(rotation = 45)
colors = ['C0','C1','C2','C3','C4','C5','C6','C7']
pyplot.bar(x,y, color=colors)
pyplot.savefig('./{0}_matplotlib.png'.format(user))

# WordCloud
title = '{0}_WordCloud'.format(user)
pyplot.title(title)
pyplot.imshow(wordcloud, interpolation='bilinear')
pyplot.axis("off")
pyplot.margins(x=0, y=0)
pyplot.savefig('./{0}_wordcloud.png'.format(user))

# 엑셀 편집
# from openpyxl import load_workbook, Workbook
# from openpyxl.drawing.image import Image
# from openpyxl.styles import Font, PatternFill, Alignment

# wb = Workbook()
# ws = wb.active

# img = Image('./{0}_matplotlib.png'.format(user))
# ws.add_image(img, "C13")

# img = Image('./{0}_wordcloud.png'.format(user))
# ws.add_image(img, "C36")

# ws['A1'] = '당근마켓 실행 결과'
# ws['A1'].font = Font(name='맑은 고딕', size=20, bold=True)
# ws.merge_cells('A1:M1')
# ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

# ws['C12'] = '카테고리 시각화'
# ws['C12'].font = Font(name='맑은 고딕', size=18, bold=True)
# ws.merge_cells('C12:K12')
# ws['C12'].alignment = Alignment(horizontal='center', vertical='center')

# ws['C35'] = '워드클라우드'
# ws['C35'].font = Font(name='맑은 고딕', size=18, bold=True)
# ws.merge_cells('C35:K35')
# ws['C35'].alignment = Alignment(horizontal='center', vertical='center')

# ws['B3'] = '간접 개인식별정보'
# ws['B3'].font = Font(name='맑은 고딕', size=13, bold=True)
# ws.merge_cells('B3:D3')
# ws['B3'].alignment = Alignment(horizontal='center', vertical='center')

# ws['B5'] = '신체적 정보'
# ws['B5'].font = Font(name='맑은 고딕', size=13, bold=True)
# ws.merge_cells('B5:D5')
# ws['B5'].alignment = Alignment(horizontal='center', vertical='center')

# ws['B7'] = '생활 프라이버시 정보'
# ws['B7'].font = Font(name='맑은 고딕', size=13, bold=True)
# ws.merge_cells('B7:D7')
# ws['B7'].alignment = Alignment(horizontal='center', vertical='center')

# highlight = PatternFill(start_color='339f46', end_color='339f46', fill_type='solid')
# ws.cell(3,2).fill = highlight
# ws.cell(5,2).fill = highlight
# ws.cell(7,2).fill = highlight
# ws.cell(12,3).fill = highlight
# ws.cell(35,3).fill = highlight

# highlight = PatternFill(start_color='ff8a3d', end_color='ff8a3d', fill_type='solid')
# for num in range(1, 14):
#     ws.cell(1,num).fill = highlight

# wb.save("result.xlsx")
# wb.close()

driver.quit()