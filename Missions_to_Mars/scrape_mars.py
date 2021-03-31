from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import os
import time

#Site Naviagation
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Defining scrape and dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

#Define marsNews
def marsNews():
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    news_html = browser.html
    soup = bs(news_html, 'lxml')
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    output = [news_title, news_paragraph]
    return output

#Define marsImage
def marsImage():
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html,"html.parser")
    image = image_soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = "https://spaceimages-mars.com/" + image
    return featured_image_url

#Define marsFacts
def marsFacts():
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    mars_facts =pd.read_html(facts_url)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df = mars_facts_df.drop(columns = [2])
    mars_facts_df = mars_facts_df.set_index(0)
    mars_facts_html = mars_facts_df.to_html(header=False, index=False)
    return mars_facts_html