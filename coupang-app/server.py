from flask import Flask,render_template
from typing import List,Dict,Union
from src.crawl import get_headers,Coupang
from datetime import datetime
import urllib.parse as rep

app : Flask = Flask(__name__)

# ===== Type Hint
PRODUCT_LIST = List[List[Dict[str,Union[str,int]]]]
# =====

# JSON
json_file : str = 'headers/headers.json'

# Headers
headers : Dict[str,str] = get_headers(json_file=json_file)

# page
page : int = 1

# query
query : str = '건전지'

# Request URL
request_urls : List[str] = [f'https://www.coupang.com/np/search?q={rep.quote_plus(query)}&channel=&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={str(page)}&rocketAll=false&searchIndexingToken=1=9&backgroundColor=' for page in range(1, page + 1 )]

# Create Coupang Instance
coupang : Coupang = Coupang(headers=headers)

# Get Product List
product_list : PRODUCT_LIST = [coupang.get_prod_list(request_url=request_url) for request_url in request_urls]

# now date
now = datetime.now()
today_date : str = f"{now.year}년 {now.month}월 {now.day}일"

# main text
main_text : str = ''

# prod rank
rank = 1

# loop
for x in product_list:
    for prod in x:
        main_text += f"""<a href={prod['link']} target='_blank'><div class="image main"><img src="{prod['img_url']}" alt="" /></div></a><p><h2>{rank}.{prod['title']}<b></h2>가격: {prod['price']}<br>평점: {prod['rating']}<br>리뷰 수: {prod['review_cnt']}</p>""".strip()
        
        rank += 1

# index.html
file_name : str = 'index.html'

# sub text
sub_text = f'오늘의 키워드 : {query}'

html_text : str = f"""
<!DOCTYPE HTML>
<!--
Massively by HTML5 UP
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
<head>
    <title>Generic Page - Massively by HTML5 UP</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="assets/css/main.css" />
    <noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
</head>
<body class="is-preload">

    <!-- Wrapper -->
        <div id="wrapper">

            <!-- Header -->
                <header id="header">
                    <a href="index.html" class="logo">Massively</a>
                </header>


            <!-- Main -->
                <div id="main">

                    <!-- Post -->
                        <section class="post">
                            <header class="major">
                                <span class="date">{today_date}</span>
                                <h1>{sub_text}</h1>
                            </header>
                            {main_text}
                        </section>
                </div>
            <!-- Copyright -->
                <div id="copyright">
                    <ul><li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li></ul>
                </div>
        </div>
    <!-- Scripts -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/jquery.scrollex.min.js"></script>
        <script src="assets/js/jquery.scrolly.min.js"></script>
        <script src="assets/js/browser.min.js"></script>
        <script src="assets/js/breakpoints.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>
</body>
</html>
""".strip()
with open(f'templates/html/{file_name}','w',encoding='UTF-8') as fp:
    fp.write(html_text)

@app.route('/')
def index():
    return render_template('html/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)