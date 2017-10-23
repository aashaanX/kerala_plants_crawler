import time
from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, urls):
    data_links = []
    for url in urls:
        driver.get(url)
        try:
            html_source = driver.page_source
            soup = bs(html_source, 'html5lib')
            href_link = []
            for link in soup.find_all('a'):
                href_link.append(link.get('href'))
            data_links = data_links + list(
                filter(lambda x: 'keralaplantsdetails.aspx?id=' in str(x),
                       href_link))
            for p_no in range(2, 19, 1):
                try:
                    driver.find_element_by_link_text(str(p_no)).click()
                except NoSuchElementException:
                    try:
                        driver.find_element_by_link_text("...").click()
                    except NoSuchElementException:
                        break
                    html_source = driver.page_source
                    soup = bs(html_source, 'html5lib')
                    href_link = []
                    for link in soup.find_all('a'):
                        href_link.append(link.get('href'))
                    data_links = data_links + list(
                        filter(
                            lambda x: 'keralaplantsdetails.aspx?id=' in str(x),
                            href_link))
                    continue
                html_source = driver.page_source
                soup = bs(html_source, 'html5lib')
                href_link = []
                for link in soup.find_all('a'):
                    href_link.append(link.get('href'))
                data_links = data_links + list(
                    filter(lambda x: 'keralaplantsdetails.aspx?id=' in str(x),
                           href_link))
        except TimeoutException:
            print(url)
    return data_links


def dataExtract(url):
    r = requests.get(url)
    soup = bs(r.content, 'html5lib')
    string = ''
    print("image url :/http://keralaplants/" + soup.find_all('img')[1]['src'])
    for link in soup.find_all('span'):
        print(link.text)


if __name__ == "__main__":
    # below urls list is for testing
    #urls = ["http://keralaplants.in/exotic-plants-kerala.aspx"]
    urls = [
        "http://keralaplants.in/exotic-plants-kerala.aspx",
        "http://keralaplants.in/garden-plants-kerala.aspx",
        "http://keralaplants.in/trees-in-kerala.aspx",
        "http://keralaplants.in/herbs-in-kerala.aspx",
        "http://keralaplants.in/shrubs-in-kerala.aspx",
        "http://keralaplants.in/climbers-in-kerala.aspx",
        "http://keralaplants.in/medicinal-plants-in-kerala.aspx"
    ]
    driver = init_driver()
    links = lookup(driver, urls)
    data_links = []
    for link in links:
        if link not in data_links:
            data_links.append(link)
    time.sleep(5)
    driver.quit()
    for data_link in data_links:
        url = 'http://keralaplants.in/' + data_link
        print(url)
        dataExtract(url)
        print('*****************************************')
