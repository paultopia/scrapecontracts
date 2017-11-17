
# coding: utf-8

# currently untested refactor


import requests, pickle, json, sklearn
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from dirtyclean import clean
from urllib.parse import urljoin
from time import sleep

# I need some debug logging here.
import logging
# logging.basicConfig(filename='scraping.log',level="DEBUG")
# removing for production, now that it works.

browheader = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"}

def fetch(link):
    sleep(1)
    logging.debug("trying to get: " + link)
    try:
        response = requests.get(link, timeout=2, headers=browheader)
    except:
        logging.debug("failed to get: " + link)
        return None
    if response.status_code == 200:
        logging.debug("successfully got: " + link)
        return BeautifulSoup(response.text, "lxml")
    return None

with open("trained_contract_model.pickle", "rb") as pm:
    model = pickle.load(pm)
with open("contract_data_transformer.pickle", "rb") as pt:
    transformer = pickle.load(pt)
with open("sites_to_scrape.json") as sj:
    sites = json.load(sj)


def isContract(newdata):
    if newdata is None:
        logging.debug("newdata is None in isContract")
        return False
    newdata = [newdata]
    transformed = transformer.transform([clean(x) for x in newdata])
    predictions = model.predict_proba(transformed)
    logging.debug("I got a prediction!  it's " + str(predictions))
    result = predictions[:,1] > 0.5
    return result[0]

def normalize_link(baseurl, href):
    if href:
        if href.startswith('http'):
            return href.partition("#")[0]
        return urljoin(baseurl, href).partition("#")[0]
    return None

def extract_links(soup, baseurl):
    if soup is None:
        return None
    return list(set([normalize_link(baseurl, x.get("href")) for x in soup.find_all('a')]))

def extract_text(soup):
    if soup is None:
        return None
    for crap in soup(["script", "style", "meta"]):
        crap.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
    
def check_for_TOS(link):
    if link:
        soup = fetch(link)
        text = extract_text(soup)
        if isContract(text):
            return {"url": link, "text": text}
    return None
    
def findTOS(site):
    site1 = "https://" + site
    site2 = "http://" + site
    site3 = "https://www." + site
    site4 = "http://www." + site
    try:
        target = site1
        soup = fetch(target)
    except:
        try:
            target = site2
            soup = fetch(target)
        except:
            try:
                target = site3
                soup = fetch(target)
            except:
                try:
                    target = site4
                    soup = fetch(target)
                except:
                    soup = None
    links = extract_links(soup, target)
    if links:
        try: 
            return [x for x in [check_for_TOS(link) for link in links] if x is not None]
        except Exception as e:
            logging.error("got error in link checking: " + str(e))
    return None

# so this exposes a simple API that I can just call from other code: loop over the sites to check and call findTOS on each.  Then for each return from that, I can check if it's none, and if not, append the contents to database. 

# or I can just stick the database code in here and have done with it. 
