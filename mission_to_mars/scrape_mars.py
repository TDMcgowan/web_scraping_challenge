import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import os

def scrape():
    browser = Browser('chrome','chromedriver')
    title, paragraph = news(browser)
    mars = {
        'title': title,
        'paragraph': paragraph,
        # 'image': image(browser),
        'facts': facts(),
        'hemispheres': hemi(browser)
    }
    
    return mars

def news(browser):
    browser.visit('https://mars.nasa.gov/news/')
    title = browser.find_by_css('div.content_title a').text
    paragraph = browser.find_by_css('div.article_teaser_body').text
    return title, paragraph

def facts():
    return pd.read_html('https://space-facts.com/mars/')[0].to_html()

def hemi(browser):
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    links = browser.find_by_css('a.itemLink h3')
    hemispheres = []
    for i in range(len(links)):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphere['url'] = browser.find_by_text('Sample')['href']
        hemispheres.append(hemisphere)
        browser.back()
    browser.quit()
    return hemispheres