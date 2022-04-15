import pandas as pd
import argparse 
import numpy as np
from tqdm import tqdm
from konlpy.tag import Okt as okt #명사 단위 형태소 분석기
from collections import Counter

#This will extract and count nouns from csv files collected by the crawler
#You can select which csv file to analyze by saying yyyymmdd 
parser = argparse.ArgumentParser(description= 'Give me the date to read articles!')
parser.add_argument('date_to_read', type=int, help = 'yyyymmdd')
args = parser.parse_args()
date_to_read = args.date_to_read

#Load the dataset
def data_initializer(date):
    print('Load dataset...')
    temp = pd.DataFrame(pd.read_csv("D:/crawling/crawling_" + str(date) + ".csv"))
    print(temp.head())
    print(temp.tail())
    return temp

def noun_analyzer(df_text):
    print('Initialize the analyzer...')
    tokenizer = okt()
    stop_words = ['기사', '뉴스', '분류', '섹션'] #These words will be filtered from the result 
    noun_temp = df_text
    print('Tokenizing start')
    noun_temp['tokenized'] = noun_temp['news'].apply(tokenizer.nouns) #Tokenizing nouns
    #Filter stop_words    
    noun_temp['tokenized'] = noun_temp['tokenized'].apply(lambda x : [item for item in x if item not in stop_words and len(item) > 1])
    print('Tokenizing successful')
    return noun_temp
        
#main code
text_item = data_initializer(date_to_read)
noun_list = noun_analyzer(text_item)
tokenized = np.hstack(noun_list['tokenized'].values)
print(tokenized)

#Word count
word_count = Counter(tokenized)
print(word_count.most_common(10))

