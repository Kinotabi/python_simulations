#뉴스 기사를 크롤링하는 프로그램
'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=2'

  #sid1=100 -> 정치 등
  #각각의 시드가 존재함

 #!pip install newspaper3k
 #!pip install beautifulsoup
 #!pip install requests
 #!pip install argparse

 #네이버 뉴스에서 기사 url 가져오기
 #url을 newspaper3k로 분석
 #분석된 내용을 데이터프레임에 저장
 #데이터프레임을 csv로 export

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse
from newspaper import Article
from datetime import datetime
from tqdm import tqdm

#initial settings
parser = argparse.ArgumentParser(description = 'Initialize crawler')
parser.add_argument('page', type = int, help = 'Set the page number')
parser.add_argument('code', type = int, help = 'Choose the category code')
parser.add_argument('date', type = int, help = 'Choose the date')

args = parser.parse_args()

page_num = args.page
code_num = args.code
date_num = args.date

headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

#Crawling part
class crawler_naver:
    def __init__(self):
        self.page = page_num
        self.code = code_num
        self.date = date_num
        self.urllist = []
        #extract news url
        for i in tqdm(range (1, self.page + 1)) :
            url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=' + str(self.code) + '&date=' + str(self.date) +'&page=' + str(i)
            #headers is the user-agent information

            #Provide website headers for saying that I'm a user
            news = requests.get(url, headers=headers)
            news.content

            #Analyze the HTML page
            #the second is the analyzer, the first is the text to be analyzed
            soup = BeautifulSoup(news.content, 'html.parser')
            news_list = soup.select('.type06_headline li dl')
            #use extend if you want to add more line to the existing lines
            news_list.extend(soup.select('.type06 li dl'))
            #just get a tag <a href = address> by using a.get('href')
            for line in news_list:
                print(line.find("a")['href'])
                self.urllist.append(line.find("a")['href'])

        #extract the main text
        print('뉴스 기사 수 : ', len(self.urllist))
        self.text_list = []
        for i in tqdm(self.urllist):
            news = Article(i, language = 'ko')
            news.download()
            news.parse()
            self.text_list.append(news.text)

        #create data frame
    def return_news(self):
        self.df = pd.DataFrame({'news' : self.text_list})
        self.df['code'] = self.code
        return self.df



#main
if __name__ == '__main__':
    todays_date = datetime.now()
    address = '/Users/mindonghwan/Documents/GitHub/python_simulations/Crawling/'
    news_data = crawler_naver()
    texts = news_data.return_news()
    texts.to_csv(address + 'crawling_' + str(todays_date) + '.csv' , sep=',', index=False, encoding='utf-8-sig')
    #Results will be a csv file with the exact date
