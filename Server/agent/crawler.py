from bs4 import BeautifulSoup
import re



class Crawler:
    def __init__(self):

        # 크롤링하려는 HTML 소스의 샘플 (div > ul > li 구조)
        self.html_doc = """
        <html>
            <head>
                <title>Home</title>
            </head>
            <body>
                <div class="section">
                    <h2>영역 제목</h2>
                        <ul> 
                            <li><a href="/news/news1">기사 제목1</a></li>
                            <li><a href="/news/news2">기사 제목2</a></li>
                            <li><a href="/news/news3">기사 제목3</a></li>
                        </ul>
                </div>
            </body>
        </html>
        """

        # 크롤링하려는 HTML 소스의 샘플 (테이블 구조)
        self.html_table = """
        <html>
            <div class="aside_section"> 
                <table class="tbl"> 
                    <thead>
                        <tr> 
                            <th scope="col">컬럼1</th> 
                            <th scope="col">컬럼2</th> 
                        </tr> 
                    </thead>
                    <tbody>
                    <tr> 
                        <th><a href="/aside1">항목1</a></th> 
                        <td>항목1값1</td> 
                        <td>항목1값2</td> 
                    </tr>
                    <tr>
                        <th><a href="/aside2">항목2</a></th> 
                        <td>항목2값1</td> 
                        <td>항목2값2</td> 
                    </tr>
                    </tbody>
                </table>
            </div>
        </html>
        """

    def get_news_section(self):
        soup = BeautifulSoup(self.html_doc, 'html.parser')  # HTML Parser "soup" Object 생성
        print(soup.prettify())  # "soup" Object의 정상적 생성을 확인
        
        print("title", soup.title) # <title> Tag 추출
        #<title>Home</title>
        
        print("title stinrg", soup.title.string) # <title> Tag안의 Contents를 추출
        #Home
        
        print("title parent name", soup.title.parent.name) # <title> Tag의 부모 Tag의 이름을 추출
        #head
        
        print("div", soup.div)
        """
        <div class="section">
        <h2>영역 제목</h2>
        <ul>
        <li><a href="/news/news1">기사 제목1</a></li>
        <li><a href="/news/news2">기사 제목2</a></li>
        <li><a href="/news/news3">기사 제목3</a></li>
        </ul>
        </div>
        """
        
        print("div class", soup.div['class'])
        #['section']
        
        print("li", soup.li)
        #<li><a href="/news/news1">기사 제목1</a></li>
        
        print("find li", soup.find_all('li'))   # 모든 <li> Tag들이 담긴 List를 반환
        #[<li><a href="/news/news1">기사 제목1</a></li>, <li><a href="/news/news2">기사 제목2</a></li>, <li><a href="/news/news3">기사 제목3</a></li>]
        
        print("find class section", soup.find_all(class_="section"))    # class Attribute 값이 "section"인 모든 Tag들이 담긴 List를 반환 (class는 예약어이므로 class_를 사용)
        """
        [<div class="section">
        <h2>영역 제목</h2>
        <ul>
        <li><a href="/news/news1">기사 제목1</a></li>
        <li><a href="/news/news2">기사 제목2</a></li>
        <li><a href="/news/news3">기사 제목3</a></li>
        </ul>
        </div>]
        """

        print("find href", soup.find_all(href=re.compile("/news"))) # href Attribute 값에 "/news"를 포함한 모든 Tag들이 담긴 List를 반환 (using Regular Expression re Module)
        #[<a href="/news/news1">기사 제목1</a>, <a href="/news/news2">기사 제목2</a>, <a href="/news/news3">기사 제목3</a>]
        
        news_list = soup.find_all(href=re.compile("/news"))  
        for news in news_list:
            print(news["href"]) # 링크
            print(news.string)  # 기사제목
        """
        /news/news1
        기사 제목1
        /news/news2
        기사 제목2
        /news/news3
        기사 제목3
        """

    def get_side(self):
        soup = BeautifulSoup(self.html_table, 'html.parser')

        print("table", soup.table)

        print("thead th", soup.thead.find_all(scope=re.compile("col"))) # <thead> Tag 내에서 scope Attribute 값에 "col"이 포함된 모든 Tag들이 담긴 List를 반환
        #thead th [<th scope="col">컬럼1</th>, <th scope="col">컬럼2</th>]

        col_list = [ col.string for col in soup.thead.find_all(scope=re.compile("col"))]    # <thead> Tag 내에서 scope Attribute 값에 "col"이 포함된 모든 Tag들의 Contents들이 담긴 리스트를 col_list에 저장
        print(col_list)
        #['컬럼1', '컬럼2']

        tr_list = soup.tbody.find_all("tr") # <tbody> Tag 내에서 모든 <tr> Tag에 담긴 항목 값들을 반환
        print("tr list", tr_list)
        """
        [<tr>
        <th><a href="/aside1">항목1</a></th>
        <td>항목1값1</td>
        <td>항목1값2</td>
        </tr>, <tr>
        <th><a href="/aside2">항목2</a></th>
        <td>항목2값1</td>
        <td>항목2값2</td>
        </tr>]
        """

        for tr in tr_list:  # tr_list에서 <td> Tag의 Contents들을 추출
            for td in tr.find_all("td"):
                print("tr td", td.string)
        """
        tr td 항목1값1
        tr td 항목1값2
        tr td 항목2값1
        tr td 항목2값2
        """                

if __name__ == "__main__":
    crawler = Crawler()
    crawler.get_news_section()
    crawler.get_side()
