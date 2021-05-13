# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 20:51:23 2021

@author: user
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import numpy as np
from tqdm import tqdm
import csv
import json
import warnings
warnings.filterwarnings(action='ignore') 

os.chdir(r'C:\Users\user\OneDrive\바탕 화면')

wd=webdriver.Chrome('chromedriver.exe')
wd.maximize_window()
wd.implicitly_wait(3)

url='https://www.melon.com/genre/song_list.htm?gnrCode=GN0500'

wd.get(url)
time.sleep(1)

df_indibob=pd.DataFrame(columns=['rank', 'img_src', 'title', 'artist', 'album_name', 'heart', 'open_date', 'category', 'lyric', 'lyric_artist', 'compose_artist', 'arrange_artist'])

for i in tqdm(range(1, 31)) :
    # 처음 페이지에서 긁는거는 beautifulsoup으로 소스 딴담에 하는게 시간이 더 빠를듯. 셀레니움은 클릭해서 세부정보 긁어올 때 쓰는거로..
    xpath=f'//*[@id="frm"]/div/table/tbody/tr[{i}]'
    rank=wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[2]/div').find_element_by_class_name('rank').text
    img_src=wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[3]/div/a/img').get_attribute("src")
    title=wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[5]/div/div/div[1]/span/a').text
    artist=wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[5]/div/div/div[2]/a').text
    album_name=wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[6]/div/div/div/a').text
    heart=wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[7]/div/button/span[2]').text
    
    wd.find_element_by_xpath(xpath).find_element_by_xpath(f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[4]/div/a').click()
    time.sleep(1)
    
    open_date=wd.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[2]').text
    category=wd.find_element_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]').text
    
    # wd.find_element_by_xpath('//*[@id="lyricArea"]/button').click()
    # time.sleep(2)
    
    lyric=wd.find_element_by_xpath('//*[@id="d_video_summary"]').text
    try :
        lyric_artist=wd.find_element_by_xpath('//*[@id="conts"]/div[3]/ul/li[1]/div[2]/div[1]/a').text
    except :
        lyric_artist=''
    
    compose_artist=wd.find_element_by_xpath('//*[@id="conts"]/div[3]/ul/li[2]/div[2]/div[1]/a').text
    
    try :
        arrange_artist=wd.find_element_by_xpath('//*[@id="conts"]/div[3]/ul/li[3]/div[2]/div[1]/a').text
    except :
        arrange_artist=''
    
    df_indibob.loc[i, 'rank']=rank
    df_indibob.loc[i, 'img_src']=img_src
    df_indibob.loc[i, 'title']=title
    df_indibob.loc[i, 'artist']=artist
    df_indibob.loc[i, 'album_name']=album_name
    df_indibob.loc[i, 'heart']=heart
    df_indibob.loc[i, 'open_date']=open_date
    df_indibob.loc[i, 'category']=category
    df_indibob.loc[i, 'lyric']=lyric
    df_indibob.loc[i, 'lyric_artist']=lyric_artist
    df_indibob.loc[i, 'compose_artist']=compose_artist
    df_indibob.loc[i, 'arrange_artist']=arrange_artist
    
    time.sleep(1)
    
    wd.back()
    time.sleep(1)

# df_indibob=df_indibob.set_index('title')
df_indibob.to_csv(r'C:\Users\user\OneDrive\바탕 화면\부동산 빅데이터 분석 스터디\과제\6주차 수업 과제\멜론 크롤링\indibob.csv', encoding='cp949')

df_indibob=pd.read_csv(r'C:\Users\user\OneDrive\바탕 화면\부동산 빅데이터 분석 스터디\과제\6주차 수업 과제\멜론 크롤링\indibob.csv', encoding='cp949')
try :
    del df_indibob['Unnamed: 0']
except : 
    pass

df_indibob=df_indibob.set_index('rank')

def make_json(csvFilePath, jsonFilePath):
    data = {}
    
    with open(csvFilePath, encoding='cp949') as csvf:
        csvReader = csv.DictReader(csvf)
         
        for rows in csvReader:
            
            key = rows['rank']
            data[key] = rows
 
    with open(jsonFilePath, 'w', encoding='utf-8-sig') as jsonf:
        jsonf.write(json.dumps(data, indent=4, ensure_ascii=False))
         
csvFilePath = r'C:\Users\user\OneDrive\바탕 화면\부동산 빅데이터 분석 스터디\과제\6주차 수업 과제\멜론 크롤링\indibob.csv'
jsonFilePath = r'C:\Users\user\OneDrive\바탕 화면\부동산 빅데이터 분석 스터디\과제\6주차 수업 과제\멜론 크롤링\json.json'
 
make_json(csvFilePath, jsonFilePath)