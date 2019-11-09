#!/usr/bin/env python
# coding: utf-8

# In[305]:


import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver


# In[306]:


executable_path = {'executable_path':'C:/Users/woodf/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
html = browser.html
soup = bs(html, 'lxml')


# In[ ]:


#get first title
results = soup.find('div', class_='content_title').text
news_title = results.strip()
news_title


# In[ ]:


#get first p
news_p = soup.find('div', class_="article_teaser_body").text
news_p


# In[ ]:


#load spaceimages into splinter and soup
url_pic = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_pic)
html2 = browser.html
soup2 = bs(html2, 'html.parser')


# In[ ]:


#clicking button element via splinter isn't working so will "click" via soup 
button = soup2.find('a', class_="button fancybox")
button_click = "https://www.jpl.nasa.gov" + button["data-link"]
button_click


# In[314]:


btcl = soup2.find('a', class_="button fancybox")["data-link"]
btcl


# In[ ]:


#use splinter to navigate to link
browser.visit(button_click)
html3=browser.html
soup3 = bs(html3, 'html.parser')


# In[ ]:


#get largesize image link
large = soup3.find('figure', class_='lede')
featured_image_url = "https://www.jpl.nasa.gov" + large.a['href']
featured_image_url


# In[284]:


#mars weather, open site in splinter and create soup object
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)
html4 = browser.html
soup4 = bs(html4, 'html.parser')


# In[285]:


#find first text paragraph and delete anchor tet
link = soup4.find('div', class_='js-tweet-text-container')
mars = link.find('a')
mars.decompose()


# In[287]:


#assign variable to weather text 
mars_weather = link.p.text
mars_weather


# In[288]:


#get table from space facts
facts_url = "https://space-facts.com/mars/"
facts_table = pd.read_html(facts_url)


# In[294]:


#create df
table_df = facts_table[1]
table_df


# In[298]:


#convert to HMTL string and clean it
html_table = table_df.to_html()
html_table = html_table.replace('\n','')


# In[300]:


#write to text
text_file = open("planet_table.html", "w")
text_file.write(html_table)
text_file.close()


# In[301]:


#hemispheres
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)
hemi_html = browser.html
hemi_soup = bs(hemi_html, 'html.parser')


# In[302]:


items = hemi_soup.find_all('div', class_='item')


#     for article in articles:
#         # Use Beautiful Soup's find() method to navigate and retrieve attributes
#         h3 = article.find('h3')
#         link = h3.find('a')
#         href = link['href']
#         title = link['title']
#         print('-----------')
#         print(title)
#         print('http://books.toscrape.com/' + href)
# 
#     # Click the 'Next' button on each page
#     try:
#         browser.click_link_by_partial_text('next')
#           
#     except:
#         print("Scraping Complete")

# In[325]:


#once again, clicking button element via splinter isn't working so will "click" via soup 
#loop through each page, create dictionary for each page and append to a hemisphere list

hemi_list = []
for item in items:
    link = item.find('a', class_ = "itemLink product-item")
    click = "https://astrogeology.usgs.gov" + link["href"]
    browser.visit(click)
    html_click = browser.html
    soup_click = bs(html_click, 'html.parser')
    title = soup_click.find('h2', class_ = "title").text.rstrip("Enhanced")
    href = soup_click.find('div', class_ = "downloads").find("li").find('a')["href"]
    click_dict = {}
    click_dict["title"] = title
    click_dict["img_url"] = href
    hemi_list.append(click_dict)

    
    


# In[328]:


#check list
hemi_list


# In[330]:


get_ipython().system('jupyter nbconvert --to script config_template.ipynb')


# In[ ]:




