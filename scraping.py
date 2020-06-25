# Import Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)

   news_title, news_paragraph = mars_news(browser)

   # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    ### Mars News

    def mars_news(browser):
        # Visit the mars nasa news site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

        # NOTE: The optional delay is useful because sometimes dynamic pages take a little while to 
        # load, especially if they are image-heavy. With the above line, we are telling our browser 
        # to wait a second before searching for components.

        # set up HTML parser
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')

        # Add try/except for error handling
        try:
            slide_elem = news_soup.select_one('ul.item_list li.slide')

            slide_elem.find("div", class_='content_title')

            # Use the parent element to find the first `a` tag and save it as `news_title`
            # NOTE: Pulls the most recent article title
            news_title = slide_elem.find("div", class_='content_title').get_text()
            news_title

            #  Replicate above to pull article summary (teaser)
            news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
            news_p

        except AttributeError:
            return None, None

        return news_title, news_p

    ### Featured Images

    def featured_image(browser):
        # Visit URL
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()

        # Find the more info button and click that
        # Splinter is searching for this element by text
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.find_link_by_partial_text('more info')
        more_info_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        try:
            # Find the relative image url
            img_url_rel = img_soup.select_one('figure.lede a img').get("src")
            img_url_rel
        except AttributeError:
            return None

        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

        return img_url

    ### Mars Facts

    def mars_facts():

        # Use pandas to read table into a df
        # By specifying an index of 0, we’re telling Pandas to pull only the first table it encounters
        # we assign columns to the new DataFrame for additional clarity
        # By using the .set_index() function, we turn the Description column into the df’s index. 
        # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
        
        try:
            # use 'read_html' to scrape facts into a df
            df = pd.read_html('http://space-facts.com/mars/')[0] 
        except BaseException:
            return None

        # Assign columns and set index
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        
        # Convert df to HTML, add bootstrap
        return df.to_html()

    # End Splinter browser session
    browser.quit()

    return data

# This last block of code tells Flask that our script is complete and 
# ready for action. The print statement will print out the results of 
# our scraping to our terminal after executing the code.
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())