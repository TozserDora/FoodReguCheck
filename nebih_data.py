from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import re


def get_nebih_data(url):
    """Get the newest NÉBIH collection's location by supplying the url of the NÉBIH's website"""
    driver = webdriver.Chrome()
    driver.get(url)
    document_block = driver.find_element(by=By.CLASS_NAME, value="portlet-msg-info")
    collections = document_block.find_elements(by=By.TAG_NAME, value="a")
    new_collection = collections[0]
    try:
        # Handle the cookie situation if needed
        cookie_button = driver.find_element(by=By.ID,
                                               value="_it_smc_liferay_privacy_web_portlet_PrivacyPortlet_okButton")
        cookie_button.click()
        new_collection.click()
        driver.implicitly_wait(3)
    except NoSuchElementException as e:
        pass
    finally:
        # Cookies or not, find the newest legislation collection
        new_collection.click()
        new_collection_url = new_collection.get_attribute("href")
        driver.implicitly_wait(3)

    # Download the new_collection.pdf into data
    response = requests.get(new_collection_url)
    with open('data/nebih_collection.pdf', 'wb') as file:
        file.write(response.content)


def find_legal_documents(pdf):
    """ Loop through the supplied pdf file and find Eurlex (and Netjogtar) links"""
    eurlex_links = []
    netjogtar_links = []

    for page in pdf:
        page_text = page.get_text()
        eurlex_links_per_page = re.findall(r'https?://eur-lex\.europa\.eu\/legal-\n?content[^\s]*', page_text)

        # If '\n' was inserted
        for i in range(len(eurlex_links_per_page)):
            eurlex_links_per_page[i] = eurlex_links_per_page[i].replace("\n", "")

        eurlex_links.extend(eurlex_links_per_page)

        # TODO: Do something with the invisible hrefs of the Netjogtar links
        netjogtar_links_per_page = re.findall(r'https?://net\.jogtar\.hu\S+', page_text)
        netjogtar_links.extend(netjogtar_links_per_page)
    pdf.close()
    return eurlex_links, netjogtar_links