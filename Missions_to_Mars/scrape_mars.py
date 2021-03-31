from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

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