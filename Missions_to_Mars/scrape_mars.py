from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import os
import time

# Defining scrape and dictionary
def scrape():
    #Site Naviagation
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    final_data = {}
    output = marsNews(browser)
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage(browser)
    final_data["mars_facts"] = marsFacts(browser)
    final_data["mars_hemisphere"] = marsHem(browser)

    return final_data

#Define marsNews
def marsNews(browser):
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    news_html = browser.html
    soup = bs(news_html, 'lxml')
    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    output = [news_title, news_paragraph]
    return output

#Define marsImage
def marsImage(browser):
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html,"html.parser")
    image = image_soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = "https://spaceimages-mars.com/" + image
    return featured_image_url

#Define marsFacts
def marsFacts(browser):
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    mars_facts =pd.read_html(facts_url)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df = mars_facts_df.drop(columns = [2])
    mars_facts_html = mars_facts_df.to_html(header=False, index=False)
    return mars_facts_html

#Define marsHem
def marsHem(browser):
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html,"html.parser")
    mars_hemisphere = []

    products = hemisphere_soup.find("div", class_="result-list")
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url ="https://marshemispheres.com/" + downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "image_url": image_url})
    return mars_hemisphere

if __name__=="__main__":
    print(scrape())
