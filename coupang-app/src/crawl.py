from typing import List,Dict,Union
from bs4 import BeautifulSoup as bs
import requests as rq
import re 
import json

PRODUCT_LIST = List[List[Dict[str,Union[str,int]]]]
DATA_LIST = List[Dict[str,Union[str,int]]]
DATA_DICT = Dict[str,Union[str,int]]

def get_headers(json_file: str) -> Dict[str,str]:
    with open(json_file,'r',encoding='UTF-8') as fp:
        headers : Dict[str,str] = json.loads(fp.read())['headers']
    return headers

class Coupang:    
    def __init__(self,headers: Dict[str,str]) -> None:
        self.headers = headers
    
    @staticmethod
    def get_soup_object(response: rq.Response) -> bs:
        return bs(response.text,'html.parser')
    
    def get_prod_list(self,request_url: str) -> DATA_LIST:
        # 데이터 저장 리스트
        data_list : DATA_LIST= []
        
        with rq.get(url=request_url,headers=self.headers) as response: 
            soup : bs = self.get_soup_object(response=response)
            
            # 상품 갯수            
            prod_list_length : int = len(soup.select('a.search-product-link'))
            
            for i in range(prod_list_length):
                # 데이터 저장 딕셔너리 
                data_dict : DATA_DICT = {}
                
                # 상품리스트
                prod_list : list = soup.select('a.search-product-link')
                
                # 상품명                
                title = prod_list[i].select_one('div.name')
                if title != None:
                    title = title.text.strip()
                else:
                    title = '-'

                # 상품링크
                link = 'https://www.coupang.com' + prod_list[i].attrs['href']
                
                # 상품 썸네일
                img_url = 'https:'
                thumbnail = prod_list[i].select_one('img.search-product-wrap-img')
                if thumbnail.get('data-img-src'):
                    img_url += thumbnail.get('data-img-src')
                else:
                    img_url += thumbnail.attrs['src']
                
                # 썸네일 크기 변경
                # img_url = img_url.replace('230x230ex','500x500')
                
                # 상품 가격
                price = prod_list[i].select_one('strong.price-value')
                if price != None:
                    price = int(re.sub('[^0-9]','',price.text.strip()))
                else:
                    price = '-'
                                
                # 상품 할인 전 가격
                dis_before_price = prod_list[i].select_one('del.base-price')
                if dis_before_price != None:
                    dis_before_price = int(re.sub('[^0-9]','',dis_before_price.text.strip()))
                else:
                    dis_before_price = '-'                
                
                # 상품 할인율
                dis_per = prod_list[i].select_one('span.instant-discount-rate')
                if dis_per != None:
                    dis_per = int(re.sub('[^0-9]','',dis_per.text.strip()))
                else:
                    dis_per = 0
                    
                # 평점
                rating = prod_list[i].select_one('em.rating')
                if rating != None:
                    rating = float(re.sub('[^0-9.]','',rating.text.strip()))
                else:
                    rating = 0
                
                # 리뷰 수
                review_cnt = prod_list[i].select_one('span.rating-total-count')
                if review_cnt != None:
                    review_cnt = int(re.sub('[^0-9]','',review_cnt.text.strip()))
                else:
                    review_cnt = 0
                
                
                # 데이터 저장
                data_dict['title'] = title
                data_dict['price'] = price
                data_dict['dis_before_price'] = dis_before_price
                data_dict['dis_per'] = dis_per
                data_dict['rating'] = rating
                data_dict['review_cnt'] = review_cnt
                data_dict['link'] = link
                data_dict['img_url'] = img_url
                data_list.append(data_dict)
                
                # 데이터 출력
                print(data_dict,'\n')
            
        return data_list