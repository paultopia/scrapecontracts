
# coding: utf-8

# In[1]:


import scrapy, pickle, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sklearn


# In[4]:


with open("trained_contract_model.pickle", "rb") as pm:
    model = pickle.load(pm)
with open("contract_data_transformer.pickle", "rb") as pt:
    transformer = pickle.load(pt)
with open("sites_to_scrape.json") as sj:
    sites = json.load(sj)


# In[11]:


from dirtyclean import clean
def isContract(newdata):
    newdata = [newdata]
    transformed = transformer.transform([clean(x) for x in newdata])
    predictions = model.predict_proba(transformed)
    result = predictions[:,1] > 0.5
    return result[0]


# In[12]:


isContract("this is a cat, kitty kitty cat meow, also here is some totally random text that hopefully isn't full of stopwords")


# In[51]:


# you know what?  Maybe I won't bother with scrapy here.  It isn't an amazing match for this kind of project.
import requests
from urllib.parse import urljoin

browheader = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"}

def normalize_link(baseurl, href):
    if href.startswith('http'):
        return href.partition("#")[0]
    return urljoin(baseurl, href).partition("#")[0]

def extract_links(page, baseurl):
    soup = BeautifulSoup(page, "lxml")
    return list(set([normalize_link(baseurl, x.get("href")) for x in soup.find_all('a')]))

def extract_text(page):
    soup = BeautifulSoup(page, "lxml")
    for crap in soup(["script", "style", "meta"]):
        crap.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
    
def check_for_TOS(link):
    try:
        response = requests.get(link, timeout=2, headers=browheader)
    except:
        return None
    if response.status_code == 200:
        text = extract_text(response.text)
        if isContract(text):
            return text
        return None
    
def findTOS(site):
    site1 = "https://" + site
    site2 = "http://" + site
    site3 = "https://www." + site
    site4 = "http://www." + site
    try:
        target = site1
        response = requests.get(target, timeout=2, headers=browheader)
    except:
        try:
            target = site2
            response = requests.get(target, timeout=2, headers=browheader)
        except:
            try:
                target = site3
                response = requests.get(target, timeout=2, headers=browheader)
            except:
                try:
                    target = site4
                    response = requests.get(target, timeout=2, headers=browheader)
                except:
                    response = None
    if response:
        if response.status_code == 200:
            links = extract_links(response.text, target)
            return [check_for_TOS(link) for link in links]

#findTOS("rulelaw.net")


# In[52]:


# ok it's a misidentification but that's ok, there will be scraping errors.  let's see how this works on a site with a tos in a link.

experiment = findTOS("www.moneycrashers.com")


# In[53]:


print(experiment)


# In[54]:


# ok, that's a bit of an issue --- I'm probably overidentifying because of the disclaimer text at bottom there.  let's try another
experiment2 = findTOS("chroniclevitae.com")
print(experiment2)


# In[55]:


# probably rate-limited me.  ugh.
experiment3 = findTOS("zyl.ai")
print(experiment3)


# In[ ]:


# sweet, that works.  I should put in a bit of a delay between requests via a time.sleep, but then I can shove it into production.
# I'm happy with some false positives, they can be filtered out by humans.

