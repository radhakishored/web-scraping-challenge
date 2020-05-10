from bs4 import BeautifulSoup as bs
import requests
import datetime
import pymongo
import pandas as pd
from splinter import Browser

import time
mars_info = {}
executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)
def scrape2():
    #from splinter import Browser
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    return "xyz"
    
def scrape():
    #from splinter import Browser
    from splinter import Browser
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = bs(html,'html.parser')
    news=soup.find_all("div", class_="list_text")
    news_item=news[0]
    print(f"Date :{news_item.contents[0].text}")
    print(f"The latest news title: {news_item.contents[1].text}")
    print(f"News paragraph: {news_item.contents[2].text}")
    mars_info['Date'] = news_item.contents[0].text
    mars_info['news_title'] = news_item.contents[1].text
    mars_info['news_paragraph'] = news_item.contents[2].text
    print("Mars News")
    print(mars_info)
    #********* MARS image 
    from splinter.browser import Browser
    browser = Browser('chrome', **executable_path)
    images_url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    main_url = 'http://www.jpl.nasa.gov'
    browser.visit(images_url)
    time.sleep(10)
    html = browser.html
    soup = bs(html,'html.parser')
    search_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    search_image_url = main_url+search_image_url
    print(search_image_url)
    mars_info['search_image_url'] = search_image_url
    # ********Twitter wether info
    weather_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_twitter_url)
    time.sleep(10)
    html_twitter = browser.html
    soup = bs(html_twitter,'html.parser')
    mars_weather_twitter = soup.find("span",class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
    print(mars_weather_twitter)
    mars_info['Weather'] = mars_weather_twitter
    # **********Mars Facts
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)
    #Use Pandas to convert data to a html table string
    mars_facts_pd = pd.read_html(url_mars_facts)
    mars_df = mars_facts_pd[0]
    #Create df
    mars_df.columns = ['Description', 'Value']
    mars_df.to_html(header=False, index=False)
    mars_df
    html_table = mars_df.to_html()
    #html_table
    mars_info['mars_facts_pd']=html_table
    # MARS Hemisphere
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    mars_hemisphere_main_url = "https://astrogeology.usgs.gov"
    browser.visit(mars_hemisphere_url)
    time.sleep(10)
    html_hemisphere = browser.html
    # Create a Beautiful Soup object
    soup = bs(html_hemisphere, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_url = []
    # Loop over results to get image urls
    for i in items:
        title = i.find("h3").text
        image_url = i.find('a', class_='itemLink product-item')["href"]
        browser.visit(mars_hemisphere_main_url+image_url)
        image_html = browser.html    
        soup = bs(image_html, 'html.parser')
        img_url = mars_hemisphere_main_url+soup.find("img", class_="wide-image")["src"]
        hemisphere_image_url.append({"title": title, "img_url": img_url})
    mars_info['hemisphere_image_url'] = hemisphere_image_url
    # Close the browser after scraping
    browser.quit()
        # Return results
    return mars_info          
       