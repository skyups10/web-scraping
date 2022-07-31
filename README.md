# Web_Scraping

#### 한국정보처리학회 ASK 2022(춘계학술발표대회) 
### 중고 거래 플랫폼에서 나타나는 개인정보 유출의 현황 및 제안
Status of personal information exposure on used trading platforms

해당 링크에서논문집을 다운로드 받은 후 논문에서 자세한 설명을 확인할 수 있습니다.
http://www.koreascience.or.kr/search.page?keywords=%EC%A4%91%EA%B3%A0%EA%B1%B0%EB%9E%98%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%97%90%EC%84%9C+%EB%82%98%ED%83%80%EB%82%98%EB%8A%94+%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4+%EC%9C%A0%EC%B6%9C+%ED%98%84%ED%99%A9+%EB%B0%8F+%EC%A0%9C%EC%95%88

---------
#### 사용한 언어 및 라이브러리
* Python
* 데이터 수집 라이브러리 : Selenium
* 데이터 전처리 및 가공 라이브러리 : Matplotlib, WordCloud
* 자연어 처리 : Konlpy(Kkma 형태소 분석기)
* GUI 라이브러리 : pyautogui

#### 실행 방법
<pre><code>python Web-Scraping.py</code></pre>

#### 실행 시 유의 사항
해당 코드를 수정하지 않고 실행 시 오류 발생할 수 있음

<pre><code>1. font_path = 'C:/Users/(글꼴 경로 설정)/NanumGothic.ttf'

2. driver = webdriver.Chrome(r"C:/Users/(ChromeDriver 경로 설정)/chromedriver.exe")

3. f = open('C:/Users/(불용어 사전 경로 설정)/stopwords.txt', 'r', encoding = 'utf-8')

4. pyplot.savefig('C:/Users/(데이터 전처리 및 가공 결과 경로 설정)/{0}_matplotlib.png'.format(user))
   pyplot.savefig('C:/Users/(데이터 전처리 및 가공 결과 경로 설정)/{0}_wordcloud.png'.format(user))</code></pre>

#### 참고 링크    
* ChromeDriver 설치 링크 : https://chromedriver.chromium.org/downloads

#### 실행시 나타나는 화면
![image](https://user-images.githubusercontent.com/70564788/172374599-d6f61b14-c1ae-47b0-b769-db74c9f41736.png)
