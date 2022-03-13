# Imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # Set up executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres":  mars_hemispheres(browser),
        "last_modified": dt.datetime.now()}

    # stop webdriver and return data
    browser.quit()
    return data

# Article  Scraping
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/excpet for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph test
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# Image Scraping

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# Table Scraping
def mars_facts():
    try:
        # use 'read_html' to scrape the facts table into df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of df
    df.columns=['Description', 'Mars','Earth']
    df.set_index('Description', inplace=True)

    # Convert df into html format, add bootstrap
    return df.to_html(classes="table table-striped")

# Challenge: function to scrape hemisphere data
def mars_hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Parse the html with soup
    html = browser.html
    mars_hemis_soup = soup(html, 'html.parser')
    mars_hemi_info = mars_hemis_soup.find_all('div', class_='description')

    for x in range(len(mars_hemi_info)):
    
        #   dictionary for information
        hemispheres = {}
    
        # Find and click the full image button
        mars_hemi_image_elem = browser.find_by_tag('h3')[x].click()
   
        # Parse the new html with soul
        html = browser.html
        one_hemi_soup = soup(html, 'html.parser')
        hemi_img_url_rel = one_hemi_soup.find('img', class_='wide-image').get('src')

        # absolute url
        hemi_img_url = url+hemi_img_url_rel
        
        # Get hemisphere title
        hemi_title = one_hemi_soup.find('h2', class_="title").text
    
        # add title and image to dictionary
        hemispheres["title"] = hemi_title
        hemispheres["image"] = hemi_img_url
        
        # add image and title to list
        hemisphere_image_urls.append(hemispheres)
    
        #return to previous page for next hemisphere
        browser.back()
        
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())