import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.firefox.options import Options as FirefoxOptions

def activate_tor_chrome_selenium(proxy_add):
    """ 
    Activate Chrome with Tor. Current workflow requires Tor to be opened first
    Uses ChromeDriverManager package to make loading of chrome much easier!
    
    Input: proxy_address
    Output: Selenium browser output 
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(proxy_add)
    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    

def activate_chrome_selenium_latest(default=True, proxy_add=None, pic=True, headless=True):
    """ 
    Activates Chrome for Selenium web scrapping, and allows for more customisations
    
    Parameters:
        default = True: Uses ChromeDriverManager for basic web scrapping
        proxy_add = None: Doesn't not use any proxy_add. Would be needed when I use Tor
        pic = True: Put False when I want to reduce load speed and not need pictures
        headless = True: Put False if I need to visually look at the frontend code

    Output: Selenium browser Object

    """
    
    if default:
        output = webdriver.Chrome(ChromeDriverManager().install())
    
    else:
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument(" --disable-gpu")
        chrome_options.add_argument(" --disable-infobars")
        chrome_options.add_argument(" -–disable-web-security")
        chrome_options.add_argument("--no-sandbox") 
        
        if proxy_add != None:
            chrome_options.add_argument(proxy_add)
        
        if pic:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
        
        if headless:
            chrome_options.add_argument("headless")

        output = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    return output