import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_book_urls_on_page(soup, book_urls_list):
    """ Getting book urls from page for NLB project"""

    for a in soup.find_all('a', href=True):
        if "catalogue" in a['href']:
            book_urls_list.append(a['href'])
    return book_urls_list

def log_in_nlb(browser, account_name, password):

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

    login_button_2 = """//*[@id="fm1"]/section[3]/input[4]"""
    browser.find_element_by_xpath(login_button_2).click()
    
    return browser
