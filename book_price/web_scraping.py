import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def activate_chrome_selenium_latest(
    proxy_add=None, 
    have_pic=True, 
    is_headless=True):
    """ 
    Activates Chrome for Selenium web scrapping, and allows for more customisations
    
    Parameters:
        proxy_add = None: Doesn't not use any proxy_add. Used for Tor
        pic = True: Put False to reduce load speed and not need pictures
        headless = True: Put False if I need to visually look at the frontend code

    Output: Selenium browser Object

    """
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("-–disable-web-security")
    chrome_options.add_argument("--no-sandbox") 
        
    if proxy_add != None:
        chrome_options.add_argument(proxy_add)
    
    if have_pic != True:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    
    if is_headless:
        chrome_options.add_argument("headless")
        chrome_options.add_argument('window-size=1200,1100')

    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)