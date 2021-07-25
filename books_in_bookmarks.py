#!/usr/bin/env python
# coding: utf-8

# ### Scraping NLB books that I have bookmarked 

# In[1]:


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from glob import glob
import pandas as pd
import numpy as np
import warnings
import pygsheets
import math
import time
import re
import os


# In[2]:


# Some notebook configs
warnings.filterwarnings('ignore')
pd.set_option('display.max_colwidth', 1000)


# In[3]:


from nlb_functions import *


# ### Clean files first 
# - If you have ran this script before, information from each book is saved as a rtf file in your local machine. 
# - To ensure that there is no overlaps, these rtf files are checked and removed everytime you re-run your script

# In[4]:


file_list = glob("*.rtf")
len(file_list)


# In[5]:


for files in file_list:
    os.remove(files)


# ### Go to start the scraping 

# In[7]:


browser = activate_chrome_selenium_latest(have_pic=False, is_headless=False)


# In[8]:


auth_csv_file = os.environ['nlb_login']

info = pd.read_csv(auth_csv_file)
account_name = info['values'][0]
password = info['values'][1]

browser = log_in_nlb(browser, account_name, password)


# ### Add hit to get number of page iterations needed 

# In[9]:


url_link = "https://www.nlb.gov.sg/mylibrary/Bookmarks"    
browser.get(url_link)
soup = bs(browser.page_source, 'html5lib')


# In[10]:


max_records = float(soup.find_all("div", text=re.compile("Showing"))[0].text.split(" ")[-2])
range_list = range(1, int(math.ceil(max_records / 20)) + 1)
range_list


# ### Loop through the pages! 

# In[11]:


book_urls_dict = dict()
for i in range_list:
    url_link = "https://www.nlb.gov.sg/mylibrary/Bookmarks?q=&s=&a=&p={}".format(i)
    browser.get(url_link)
    soup = bs(browser.page_source, 'html5lib')
    book_urls_dict[i] = list(set(get_book_urls_on_page(soup)))


# In[12]:


all_book_url_lists = list()
for i in range(1, len(book_urls_dict) + 1):
    all_book_url_lists = all_book_url_lists + book_urls_dict[i]


# In[13]:


final_table = pd.DataFrame()


# #### Note
# - This is a troublsome script to go to each link that I have, and see if I am on the link with the correct book info. If not, it means that I still need to do more clickings.
# - **Brace yourself.** Because this portion of the code goes through each book to get the relevant information, this part can be quite slow if you have quite a few books in your bookmark

# In[14]:


# Write iteration count
for i, urls in enumerate(all_book_url_lists):
    browser.get(urls)
    book = bs(browser.page_source, 'html5lib')
    time.sleep(3)

    try:
        link_on_book = """//*[@id="result-content-grid"]/div/div/div/div[2]/h5/a"""
        browser.find_element_by_xpath(link_on_book).click()
    except:
        pass

    link_on_availability = """//*[@id="mainContent"]/div[3]/div[2]/div[3]/div[1]/div/div/div[1]/a"""
    browser.find_element_by_xpath(link_on_availability).click()
    time.sleep(3)
    
    book = bs(browser.page_source, 'html5lib')
    with open("{}.rtf".format(urls.split('=')[-1]), "wb") as text_file:
        text_file.write(book.encode('utf-8'));


# ### Taking locally saved files and loading into Google 

# In[15]:


file_list = glob("*.rtf")
len(file_list)


# In[16]:


final_table = pd.DataFrame()
for files in file_list:
    with open(files, encoding="utf8") as f:
        book = bs(f.read())

    for i in book.find(class_= 'table table-stacked'):

        lib = list()
        code = list()
        avail = list()

        for tr in i.find_all('tr'):
            for td in tr.find_all('td'):
                tmp = td.text
                if tmp.split(" ")[-1] == 'Library' or 'library' in tmp or "Repository Used Book" in tmp or 'LLiBrary' in tmp:
                    if '.' not in tmp:
                        lib.append(tmp)
                elif 'English' in tmp or 'Chinese' in tmp:
                    code.append(tmp)
                elif 'Available' == tmp or 'Onloan' in tmp or 'Transit' in tmp or "For Reference Only" in tmp or "Reserved" == tmp:
                    avail.append(tmp)

        try:
            len(lib) == len(code) == len(avail)
        except:
            print("Error in length")
        
        book_table = pd.DataFrame([lib, code, avail]).T
        book_table['title'] = book.find('title').get_text()

        final_table = final_table.append(book_table)


# In[17]:


len(final_table.title.drop_duplicates().tolist())


# In[18]:


final_table.columns = ['library', "number", "availability", 'title']
final_table = final_table[['library', 'title', 'number', 'availability']]


# ### Thinking about how to include testing into my script

# In[19]:


# final_table[~final_table.availability.isin(['Available', 'For Reference Only'])]


# ### Thinking about testing my code 

# In[20]:


final_table[final_table.availability.isnull()].shape


# In[21]:


final_table[final_table['number'].isnull()].shape


# ### Processing 

# In[22]:


final_table.title = [i.split(" | ")[0] for i in final_table.title]
final_table['number'] = [i.replace("English", "").replace("Chinese", "") for i in final_table['number']]
final_table.loc[final_table.library == "Repository Used Book Collection", 'availability'] = "For Reference Only"
final_table['availability'] = [i.replace("Onloan - Due: ", "") for i in final_table['availability']]


# In[23]:


final_table['title'] = [i.split(r"/")[0].strip() for i in final_table['title']]


# In[24]:


ffinal_table = final_table[(final_table.library=="Bishan Public Library")]
ffinal_table = ffinal_table.sort_values('availability')
ffinal_table.shape


# ### Cleaning Bookmarks Sheet 

# In[25]:


google_auth = os.environ['gsheet_cred']
gc = pygsheets.authorize(service_file=google_auth)
sh = gc.open('NLB Project')


# ### Checking just Bishan library

# In[26]:


bishan = sh.worksheet_by_title("Bookmarks")
bishan.clear('A2:E1000')

bishan_table = final_table[final_table.library.str.contains("Bishan")]
bishan.set_dataframe(bishan_table,(1,1))


# ### Checking in all libraries

# In[27]:


all_ = sh.worksheet_by_title("All")
all_.clear('A2:F1000') 

all_.set_dataframe(final_table,(1,1))


# ### [Link](https://docs.google.com/spreadsheets/d/1s5oYU59jyU_QO3IIhCClyWGoC_MpW9L_h4l4djDUKO0/edit#gid=1021888748) to my Google Sheet
