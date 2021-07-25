#!/usr/bin/env python
# coding: utf-8

# ### Scraping NLB to know the books that I borrowed

# In[1]:


import re
import os
import time

import warnings
import pygsheets
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs

# Some notebook configs
warnings.filterwarnings('ignore')
pd.set_option('display.max_colwidth', 1000)


# #### Load in self created functions 

# In[2]:


from nlb_functions import *


# In[3]:


browser = activate_chrome_selenium_latest(is_headless=False)


# ### Log in first! 

# In[4]:


auth_csv_file = os.environ['nlb_login']

info = pd.read_csv(auth_csv_file)
account_name = info['values'][0]
password = info['values'][1]

browser = log_in_nlb(browser, account_name, password)


# ### Loop through the pages! 

# In[5]:


loans_link = "https://www.nlb.gov.sg/mylibrary/Loans"
browser.get(loans_link)

time.sleep(5)

soup = bs(browser.page_source, "html5lib")


# In[6]:


table_col = list()
table_cells = list()

for table in soup.find_all("table", class_="table table-bordered table-striped table-list"):
    for row in table.find_all('th'):
        table_col.append(row.text)
    
    for row in table.find_all('td'):
        table_cells.append(row.text)

table_col = table_col[:5]


# In[7]:


browser.close()


# ### Preparing raw data to push into G Drive

# In[8]:


books = pd.DataFrame(np.array(table_cells).reshape(int(len(table_cells)/5), 5))

books.columns = ['no', 'title', 'code', 'due', 'renewed']
books = books[['title', 'code', 'due']]

for i in ['title', 'code', 'due']:
    books[i] = [re.sub(' +', ' ', i.replace("\n", "")).strip() for i in books[i]]

books['title'] = [i.replace("Title: ", "").strip() for i in books['title']]
books['code'] = [i.replace("Barcode: ", "").strip() for i in books['code']]
books['due'] = [i.replace("Due on ", "") .strip() for i in books['due']]


# In[9]:


books


# ### Authenticate into G Drive and push data into G Drive

# In[10]:


google_auth = os.environ['gsheet_cred']
gc = pygsheets.authorize(service_file=google_auth)

sh = gc.open('NLB Project')
wks = sh.worksheet_by_title("Current_borrowed")
wks.clear('A2:D17')

wks.update_value('D2', "=ARRAYFORMULA(C2:C{}-E1)".format(books.shape[0] + 1))
wks.update_value('C19', "Average:")
wks.update_value('D19', "=AVERAGE(D2:17)")

wks.set_dataframe(books,(1,1))


# ### [Link](https://docs.google.com/spreadsheets/d/1s5oYU59jyU_QO3IIhCClyWGoC_MpW9L_h4l4djDUKO0/edit#gid=1021888748) to my Google Sheet
