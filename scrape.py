from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import time


def check_eurlex_docs(list_of_docs):
    """ Creates a dictionary with the document's parameters; name, in_force, is_up_to_date, new_version, date_of_change,
     end_date, repealed_by. The input must be a list of Eurlex links."""
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration to prevent issues
    driver = webdriver.Chrome()
    results = []
    for doc in list_of_docs:
        driver.get(doc)
        try:
            name = driver.find_element(by=By.ID, value="title").text

            doc_result = {
                "name": name,
                "in_force": None,
                "is_up_to_date": None,
                "new_version": None,
                "date_of_change": None,
                "end_date": None,
                "repealed_by": None
            }
            # Grab the single line that interests us
            force_indicator = driver.find_element(by=By.CLASS_NAME, value="forceIndicator")

            # If the document is in force and up-to-date
            if force_indicator.text == "Hatályos" or force_indicator.text == "In force":
                doc_result["in_force"] = True
                doc_result["is_up_to_date"] = True

            # If the document is in force, but not up-to-date
            elif any(kw in force_indicator.text for kw in ["Hatályos: Ez a jogi aktus módosult.",
                                                           "In force: This act has been changed."]):
                new_version_location = force_indicator.find_element(by=By.TAG_NAME, value="a")
                new_link = new_version_location.get_attribute("href")
                date_of_change = new_version_location.text
                doc_result["in_force"] = True
                doc_result["is_up_to_date"] = False
                doc_result["new_version"] = new_link
                doc_result["date_of_change"] = date_of_change

            # If the document is no longer in force
            else:
                end_date_full = force_indicator.text
                end_date = re.search(r"\d{2}/\d{2}/\d{4}", end_date_full).group()
                repeal_location = force_indicator.find_element(by=By.TAG_NAME, value="a")
                repealed_by_link = repeal_location.get_attribute("href")
                doc_result["in_force"] = False
                doc_result["end_date"] = end_date
                doc_result["repealed_by"] = repealed_by_link

            results.append(doc_result)
            time.sleep(5)
        except NoSuchElementException:
            continue
    return results


