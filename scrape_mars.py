from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup to grab the articles and teaser bodies. Create a list of dictionaries with the article and their teaser body
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('div', class_="content_title")
    article_list = []
    for article in articles:
        print(article.text)
        article_list.append(article.text)

    paragraphs = soup.find_all('div', class_="article_teaser_body")
    paragraph_list = []
    for paragraph in paragraphs:
        print(paragraph.text)
        paragraph_list.append(paragraph.text)

    articles_dict_list = []
    for i in range(len(article_list)):
        ith_dict = {}
        ith_dict.update([('headline', article_list[i]), ('teaser_body', paragraph_list[i])])
        articles_dict_list.append(ith_dict)

    #Find Featured Mars Image
    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image = soup.find('img', class_='headerimage fade-in')['src']

    featured_image_url = url2 + '/' + featured_image

    #Scrape facts about Mars from table
    url3 = 'https://galaxyfacts-mars.com/'
    browser.visit(url3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    scraped_table = str(soup.find('table', class_='table table-striped'))

    #Mars Hemispheres

    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    mars_hemis = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    mars_hemis_dict_list = []
    for x in range(len(mars_hemis)):
        
        browser.links.find_by_partial_text(mars_hemis[x]).click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        hemi_image = soup.find_all('a', string='Sample')[0]['href']
        mars_hemis_dict = {}
        mars_hemis_dict['hemisphere'] = mars_hemis[x] + ' Hemisphere'
        mars_hemis_dict['image_url'] = url4 + hemi_image
        browser.links.find_by_partial_text('Back').click()
        mars_hemis_dict_list.append(mars_hemis_dict)

    scraped_mars_data = {"articles": articles_dict_list,
                     "featured_image": featured_image_url,
                     "mars_hemispheres": mars_hemis_dict_list,
                     "mars_table": scraped_table}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return scraped_mars_data