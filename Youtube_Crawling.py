#!/usr/bin/env python
# coding: utf-8

# In[24]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('C:\\Users\82104\python level2\chromedriver.exe')


# In[2]:


driver.get("http://www.youtube.com")
driver.implicitly_wait(time_to_wait=2)
driver.maximize_window()


# In[3]:


# 올해안의 동영상 조회수 순으로 나열
def youtube_searching(word):
    url = 'https://www.youtube.com/results?search_query=' + word+'&sp=CAMSBAgFEAE%253D'
    return url


# In[4]:


word = "햄버거"
url = youtube_searching(word)
driver.get(url)


# In[6]:


import time
body = driver.find_element_by_tag_name('body')
num_of_pagedowns = 30
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    num_of_pagedowns -= 1


# In[7]:


# 웹페이지의 html 다운로드
html = driver.page_source


# In[8]:


from bs4 import BeautifulSoup
page = BeautifulSoup(html,'html.parser')


# In[9]:


# 제목
import unicodedata

title = page.find('a',attrs = {"id":"video-title"}).get_text().strip()
title =  unicodedata.normalize('NFC',title)
title


# In[10]:


#채널명
channel = page.find('a',attrs = {"class":"yt-simple-endpoint style-scope yt-formatted-string"}).get_text()
channel


# In[11]:


# 조회수
views = page.find('span',attrs = {"class":"style-scope ytd-video-meta-block"}).get_text()
views


# In[12]:


# # 영상길이
lengths = page.find('span',attrs = {"class":"style-scope ytd-thumbnail-overlay-time-status-renderer"}).get_text().strip()
lengths


# In[13]:


# all_videos
videos = page.select('#contents > ytd-video-renderer')
videos


# In[14]:


# 데이터 가져오기
def get_content(driver,video):
    # 1. 현재 페이지 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    # 2. 제목 가져오기
    title = video.find('a',attrs = {"id":"video-title"}).get_text().strip()
    #채널명
    channel = video.find('a',attrs = {"class":"yt-simple-endpoint style-scope yt-formatted-string"}).get_text()
    # 조회수
    views = video.find('span',attrs = {"class":"style-scope ytd-video-meta-block"}).get_text()
    # 영상길이
    lengths = video.find('span',attrs = {"class":"style-scope ytd-thumbnail-overlay-time-status-renderer"}).get_text().strip()
    # 수집한 정보 저장하기
    
    data = [title,channel,lengths,views]
    return data


# In[15]:


# all
results = []
for video in videos:
    data = get_content(driver,video)
    results.append(data)


# In[16]:


# 날짜 리스트
dates=[]
for i in range(len(videos)):
    date = page.select('#metadata-line > span')[2*i+1].text.strip()
    dates.append(date)


# In[17]:


import pandas as pd 
result_df = pd.DataFrame(results)
dates_df = pd.DataFrame(dates)
results2 = pd.concat([result_df,dates_df],axis =1)
results2.columns = ['title','channelName','length','views','date']
results2


# In[18]:


results2.to_excel('./files/'+word+'_crawling.xlsx')


# In[19]:


# 조회수 높은 영상이 많은 채널분류 
from collections import Counter
channelNames = []
for i in results2['channelName']:
    channelNames.append(i)
channelNames_count = Counter(channelNames)
most_channel = channelNames_count.most_common(10)
most_channel_df = pd.DataFrame(most_channel)
most_channel_df
most_channel


# In[20]:


# 채널명 리스트화
channel_names =[]
for i in range(0,10):
    channel_names.append(most_channel[i][0])


# In[21]:


# 채널명 검색
def youtuber_searching(유튜버):
    url = 'https://www.youtube.com/results?search_query=' + 유튜버
    driver.get(url)
    time.sleep(2)


# In[22]:


# 구독자 수 
html = driver.page_source
page = BeautifulSoup(html,'html.parser')
num_subscribers = page.find('span',attrs = {"id":"subscribers"}).get_text().strip().split(' ')[1]


# In[25]:


# channel_names 전체 구독자수 list화
bychannel_subscriber_num = []
for i in channel_names:
    youtuber_searching(i)
    html = driver.page_source
    page = BeautifulSoup(html,'html.parser')
    try:
        num_subscribers = page.find('span',attrs = {"id":"subscribers"}).get_text().strip().split(' ')[1]
    except:
        num_subscribers = '표시안함'
    bychannel_subscriber_num.append(num_subscribers)


# In[26]:


bychannel_subscriber_num_df = pd.DataFrame(bychannel_subscriber_num)
most_channel_df= pd.concat([most_channel_df,bychannel_subscriber_num_df],axis =1)
most_channel_df.columns = ['channel','frequency','subscribers']
most_channel_df


# In[27]:


titles = []
for i in results2['title']:
    titles.append(i)
str(titles)


# In[28]:


import re
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]' , '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', cleaned_text)
    return cleaned_text
titles2=[]
for i in titles:
    titles2.append(clean_text(i))
# only_BMP_pattern = re.compile("["
#         u"\U00010000-\U0010FFFF"  #BMP characters 이외
#                            "]+", flags=re.UNICODE)
# print(only_BMP_pattern.sub(r'', str(titles)))
titles2


# In[182]:


# 형태소 분해
import numpy as nb
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[1]:


# konlpy 설치
import konlpy as kl
kl.__version__


# In[ ]:




