import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def activate_chrome_selenium_latest(proxy_add=None, have_pic=True, is_headless=True):
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
    chrome_options.add_argument(" --disable-gpu")
    chrome_options.add_argument(" --disable-infobars")
    chrome_options.add_argument(" -–disable-web-security")
    chrome_options.add_argument("--no-sandbox") 
        
    if proxy_add != None:
        chrome_options.add_argument(proxy_add)
    
    if have_pic != True:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    
    if is_headless:
        chrome_options.add_argument("headless")

    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


def get_book_urls_on_page(soup):
    """ Getting book urls from page for NLB project 
    Args: BeautifulSoup Object
    Returns: List of book urls (list)
    
    """

    book_urls_list = list()
    for a in soup.find_all('a', href=True):
        if "catalogue" in a['href']:
            book_urls_list.append(a['href'])
    return book_urls_list

def log_in_nlb(browser, account_name, password):
    """ Authenticates into the NLB app
        Args:
            - Selenium Browser Object
            - NLB account name (str)
            - NLB account password (str)

        Returns: Selenium Browser Object
    """

    login_page = 'https://cassamv2.nlb.gov.sg/cas/login'
    browser.get(login_page)

    time.sleep(1)

    # Actions on login page
    username_tag = """//*[@id="username"]"""
    element = browser.find_element_by_xpath(username_tag)
    element.send_keys("{}".format(account_name))

    time.sleep(1)

    password_tag = """//*[@id="password"]"""
    element = browser.find_element_by_xpath(password_tag)
    element.send_keys("{}".format(password))

    time.sleep(1)

    login_button_2 = """//*[@id="fm1"]/section/input[4]"""
    browser.find_element_by_xpath(login_button_2).click()
    
    return browser
