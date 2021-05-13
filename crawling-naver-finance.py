# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 00:35:25 2021

@author: user
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings(action='ignore') 
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc
import matplotlib.ticker as ticker

os.chdir(r'C:\Users\user\OneDrive\바탕 화면')

wd=webdriver.Chrome('chromedriver.exe')
wd.maximize_window()
wd.implicitly_wait(2)

wd.get('https://finance.naver.com/')
time.sleep(1)

stock_name=input('종목명을 입력해주세요 : ')

wd.find_element_by_xpath('//*[@id="stock_items"]').send_keys(stock_name)

wd.find_element_by_xpath('//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/button').click()
time.sleep(2)

item_code=wd.find_element_by_xpath('//*[@id="middle"]/div[1]/div[1]/div/span[1]').text
item_main_url=wd.current_url

#%% 
# 시세 정보 - 시가, 고가, 저가 없는 version

# wd.find_element_by_xpath('//*[@id="content"]/ul/li[4]/a').click()
# time.sleep(1)

# stock_df=pd.DataFrame(columns=['날짜', '종가', '전일비', '등락률', '거래량', '기관', '외국인'])

# page_list=[1,2,3,4,5]

# num_list=[4,5,6,7,8, 12,13,14,15,16, 20,21,22,23,24, 28,29,30,31,32]

# index_count=1

# for i in page_list :
#     if i==2 :
#         wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[2]/tbody/tr/td[{i}]/a').click()
#         time.sleep(2)
        
#     elif i>2 :
#         wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[2]/tbody/tr/td[{i+1}]/a').click()
#         time.sleep(2)
        
#     for j in num_list :
        
#         b_date=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[1]/span').text
#         b_price=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[2]/span').text
#         b_gap=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[3]/span').text
#         b_gap_rate=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[4]/span').text
#         b_volume=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[5]/span').text
#         b_institution=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[6]/span').text
#         b_foreigner=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[7]/span').text
        
#         stock_df.loc[index_count, '날짜']=b_date
#         stock_df.loc[index_count, '종가']=b_price
#         stock_df.loc[index_count, '전일비']=b_gap
#         stock_df.loc[index_count, '등락률']=b_gap_rate
#         stock_df.loc[index_count, '거래량']=b_volume
#         stock_df.loc[index_count, '기관']=b_institution
#         stock_df.loc[index_count, '외국인']=b_foreigner
        
#         index_count+=1

#%% 
# 시세 정보 - 시가, 고가, 저가 있는 version

wd.get(f'https://finance.naver.com/item/sise_day.nhn?code={item_code}')
time.sleep(1)

stock_df=pd.DataFrame(columns=['날짜', '종가', '전일비', '시가', '고가', '저가', '거래량'])

page_list=[1,2,3,4,5,6,7,8,9,10]

num_list=[3,4,5,6,7, 11,12,13,14,15]

index_count=1

for i in page_list :
    if i==2 :
        wd.find_element_by_xpath(f'/html/body/table[2]/tbody/tr/td[{i}]/a').click()
        time.sleep(2)

    elif i>2 :
        wd.find_element_by_xpath(f'/html/body/table[2]/tbody/tr/td[{i+1}]/a').click()
        time.sleep(2)
        
    for j in num_list :
        b_date=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[1]/span').text
        b_price=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[2]/span').text
        b_gap=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[3]/span').text
        b_start=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[4]/span').text
        b_high=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[5]/span').text
        b_low=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[6]/span').text
        b_volume=wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[7]/span').text
        
        stock_df.loc[index_count, '날짜']=b_date.replace('.', '')
        stock_df.loc[index_count, '종가']=b_price.replace(',', '')
        try :
            stock_df.loc[index_count, '전일비']=b_gap.replace(',', '')
            try:
                p_m = wd.find_element_by_xpath(f'/html/body/table[1]/tbody/tr[{j}]/td[3]/span').get_attribute('class')
                if 'red' in p_m:
                    stock_df.loc[index_count, '전일비']=int(stock_df.loc[index_count, '전일비'])
                else :
                    stock_df.loc[index_count, '전일비']=int(stock_df.loc[index_count, '전일비']) * (-1)
                    
            except :
                pass
            
        except :
            pass
        
        stock_df.loc[index_count, '시가']=b_start.replace(',', '')
        stock_df.loc[index_count, '고가']=b_high.replace(',', '')
        stock_df.loc[index_count, '저가']=b_low.replace(',', '')
        stock_df.loc[index_count, '거래량']=b_volume.replace(',', '')
        
        index_count+=1

stock_df.index=pd.to_datetime(stock_df['날짜'], format='%Y%m%d')
stock_df[['종가', '전일비', '시가', '고가', '저가', '거래량']]=stock_df[['종가', '전일비', '시가', '고가', '저가', '거래량']].astype(int)
del stock_df['날짜']
stock_df=stock_df.sort_values(by='날짜')

# x 값을 day로 설정
# day_list = range(len(stock_df))
# name_list = []
# for day in stock_df.index:
#     name_list.append(day.strftime('%d'))

# x 값을 week(월요일)로 설정
day_list = []
name_list = []

for i, day in enumerate(stock_df.index):
    if day.dayofweek == 0: # dayofweek은 월요일(0)을 기준으로 숫자를 return
        day_list.append(i)
        name_list.append(day.strftime('%m.%d'))

stock_df['5일선'] = stock_df['종가'].rolling(5).mean()
stock_df['10일선'] = stock_df['종가'].rolling(10).mean()
stock_df['20일선'] = stock_df['종가'].rolling(20).mean()
stock_df['60일선'] = stock_df['종가'].rolling(60).mean()

stock_df.to_csv(f'C:/Users/user/OneDrive/바탕 화면/부동산 빅데이터 분석 스터디/과제/6주차 수업 과제/{stock_name} 일별 시세.csv', encoding='cp949')

color_fuc = lambda x : 'r' if x >= 0 else 'b'

# 색깔 구분을 위한 함수를 apply 시켜 Red와 Blue를 구분한다.
color_df = stock_df['전일비'].apply(color_fuc)

# 구분된 값을 list 형태로 만들어준다.
color_list = list(color_df)

#%%
# 차트 그리기

from matplotlib import font_manager, rc
font_path = 'C:\\Users\\user\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NanumBarunpenR.ttf'
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

from matplotlib import gridspec

fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(nrows=2, ncols=1,     
                       height_ratios=[5, 1]) 

ax=plt.subplot(gs[0])

ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

ax.plot(stock_df.index.strftime('%m.%d'), stock_df['5일선'], label='5일선')
ax.plot(stock_df.index.strftime('%m.%d'), stock_df['10일선'], label='10일선')
ax.plot(stock_df.index.strftime('%m.%d'), stock_df['20일선'], label='20일선')
ax.plot(stock_df.index.strftime('%m.%d'), stock_df['60일선'], label='60일선')

candlestick2_ohlc(ax, stock_df['시가'], stock_df['고가'], stock_df['저가'], stock_df['종가'], width=0.5, colorup='r', colordown='b')
ax.legend(loc='best')
ax.legend(fontsize=15)
ax.set_title(f'{stock_name} 일봉 차트', fontsize=25)

ax2=plt.subplot(gs[1])

ax2.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax2.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))
ax2.bar(stock_df.index.strftime('%m.%d'), stock_df['거래량'], width=0.8, color=color_list)

ax2.plot()

plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.show()

os.chdir(r'C:\Users\user\OneDrive\바탕 화면\부동산 빅데이터 분석 스터디\과제\6주차 수업 과제')
fig.savefig(f'{stock_name} 일봉 차트')

#%%
# 뉴스

wd.get(f'https://finance.naver.com/item/news_news.nhn?code={item_code}&page=&sm=title_entity_id.basic&clusterId=')
time.sleep(1)

news_df=pd.DataFrame(columns=['날짜', '제목', 'URL', '정보제공']) 

index_count=1

for x in range(1,4) :
    i=1
    ori_count=10
    
    if x==2 :
        wd.find_element_by_xpath('/html/body/div/table[2]/tbody/tr/td[2]/a').click()
    
    elif x>2 :
        wd.find_element_by_xpath(f'/html/body/div/table[2]/tbody/tr/td[{x+1}]/a').click()
        
    while i<=ori_count :
        news_date=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i}]/td[3]').text
        news_title=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i}]/td[1]/a').text
        news_url=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i}]/td[1]/a').get_attribute('href')
        news_info_from=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i}]/td[2]').text
        
        news_df.loc[index_count, '날짜']= news_date
        news_df.loc[index_count, '제목']= news_title
        news_df.loc[index_count, 'URL']= news_url
        news_df.loc[index_count, '정보제공']= news_info_from
        
        index_count+=1
        
        try :
            news_more_title=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[1]/td[1]/a') # i+1번째 타이틀을 긁어서 읽히는지 보기
            try :
                news_more=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/div/a').click() # 더보기 버튼이 있는지 확인
                time.sleep(1)
                news_more_count=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/div/a/em').text
                
                for j in range(1, news_more_count+2):
                    news_more_date= wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[{j}]/td[3]').text
                    news_more_title= wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[{j}]/td[1]/a').text
                    news_more_url= wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[{j}]/td[1]/a').get_attribute('href')
                    news_more_inf_from= wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[{j}]/td[2]').text
                    
                    news_df.loc[index_count, '날짜']= news_more_date
                    news_df.loc[index_count, '제목']= news_more_title
                    news_df.loc[index_count, 'URL']= news_more_url
                    news_df.loc[index_count, '정보제공']= news_more_info_from
                    
                    index_count+=1
                    i+=1
                    ori_count+=1
                
            except :
                news_more_date=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[1]/td[3]').text
                news_more_title=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[1]/td[1]/a').text
                news_more_url=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[1]/td[1]/a').get_attribute('href')
                news_more_info_from=wd.find_element_by_xpath(f'/html/body/div/table[1]/tbody/tr[{i+1}]/td/table/tbody/tr[1]/td[2]').text
                
                news_df.loc[index_count, '날짜']= news_more_date
                news_df.loc[index_count, '제목']= news_more_title
                news_df.loc[index_count, 'URL']= news_more_url
                news_df.loc[index_count, '정보제공']= news_more_info_from
                
                index_count+=1
                i+=1
                ori_count+=1
            
        except :
            pass
        
        i+=1

news_df.to_csv(f'C:/Users/user/OneDrive/바탕 화면/부동산 빅데이터 분석 스터디/과제/6주차 수업 과제/{stock_name} 뉴스 정보.csv', encoding='cp949')

#%%
# 종토방

wd.get(item_main_url)
wd.find_element_by_xpath('//*[@id="content"]/ul/li[7]/a').click()
time.sleep(2)

discussion_df=pd.DataFrame(columns=['날짜', '제목', '글쓴이', '조회수', '공감', '비공감'])
discussion_list=[3,4,5,6,7, 9,10,11,12,13, 15,16,17,18,19, 21,22,23,24,25]
index_count=1 
page_count=1
i=1
sexy_count=1

while page_count<51 :
    
    if i==2 :
        wd.find_element_by_xpath('//*[@id="content"]/div[2]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/a').click()
        i+=1
        
    elif (i>2) & (i<11) & (sexy_count==1):
        wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[{i+1}]/a').click()
        i+=1
    
    elif (i==11) & (sexy_count==1) :
        wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[{i+1}]/a').click()
        sexy_count+=1
        i=3
    
    elif (i>2) & (i<12) & (sexy_count>1) :
        wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[{i+1}]/a').click()
        i+=1
    
    elif (i==12) & (sexy_count>1) :
        wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[{i+1}]/a').click()
        sexy_count+=1
        i=3
        
        
    for j in discussion_list :
        date=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[1]/span').text
        title=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[2]/a').text
        writer=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[3]').text
        hits=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[4]/span').text
        agree=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[5]/strong').text
        disagree=wd.find_element_by_xpath(f'//*[@id="content"]/div[2]/table[1]/tbody/tr[{j}]/td[6]/strong').text
        
        discussion_df.loc[index_count, '날짜']=date
        discussion_df.loc[index_count, '제목']=title
        discussion_df.loc[index_count, '글쓴이']=writer
        discussion_df.loc[index_count, '조회수']=hits
        discussion_df.loc[index_count, '공감']=agree
        discussion_df.loc[index_count, '비공감']=disagree
        
        index_count+=1
            
    if i==1 :
        i+=1
        
    page_count+=1

discussion_df.to_csv(f'C:/Users/user/OneDrive/바탕 화면/부동산 빅데이터 분석 스터디/과제/6주차 수업 과제/{stock_name} 종토방.csv', encoding='cp949')
