from bs4 import BeautifulSoup as bs
import lxml.html as lh
import pandas as pd
import requests
from selenium import webdriver
from splinter import Browser
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/cephra.stuart/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

webpage_info = {}
# # NASA Mars News

# In[5]:


def mars_news():
    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the title of the first story
    news_title = soup.find("div", {"class": "content_title"}).get_text(strip=True)
    
    # Get the paragraph of the first story
    news_p = soup.find("div", {"class": "article_teaser_body"}).get_text(strip=True)

 
    # Store data in a dictionary
    webpage_info['news_title'] = news_title
    webpage_info["news_p"] = news_p
    

    # Close the browser after scraping
    browser.quit()

# # JPL Mars Space Images - Featured Image


def mars_images():
    browser = init_browser()

    # Visit nasa mars space images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the url of featured image
    featured_image_data = soup.find("a", {'class': 'button fancybox'})
    image_link = featured_image_data['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov'+image_link

    # Close the browser after scraping
    browser.quit()

    # Add results to dictionary
    webpage_info['featured_image_url'] = featured_image_url


# # Mars Weather


def mars_weather():
    browser = init_browser()

    # Visit mars twitter page
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the text of first tweet
    latest_tweet = soup.find("div", {'class': 'js-tweet-text-container'}).get_text(strip=True)

    # Close the browser after scraping
    browser.quit()

    # Add results to dictionary
    webpage_info['latest_tweet'] = latest_tweet

# # Mars Facts


def mars_facts():
    browser = init_browser()

    # Visit space facts
    url = "http://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the tables from page
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Values']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()

    # Close the browser after scraping
    browser.quit()

    # Add to dictionary
    webpage_info['table'] = html_table



# # Mars Hemispheres

def mars_hemispheres():
    browser = init_browser()

    # Visit mars hemisphere page
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the text of first tweet
    hemispheres = soup.find_all("a", {'class': 'itemLink product-item'})
    hemisphere_group = []
    for item in hemispheres:
        link = item['href']
        title = item.get_text(strip=True)
        browser.visit(f'https://astrogeology.usgs.gov'+link)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url_1 = soup.find('img', {'class':'wide-image'})
        img_url = f'https://astrogeology.usgs.gov'+img_url_1['src']
        if title != "":
            hemisphere_group.append(tuple((title, img_url)))
    
    webpage_info['hemispheres'] = hemisphere_group
    
   # for item in hemispheres:
        #link = item['a']['href']
        #title = item['']
        #next_link = f'https://www.jpl.nasa.gov'+image_link
    # Close the browser after scraping
    browser.quit()

def get_data():
    mars_news()
    mars_images()
    mars_weather()
    mars_facts()
    mars_hemispheres()
    return webpage_info
