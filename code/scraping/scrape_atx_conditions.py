from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import os

RAW_DIR = os.path.join("data", "raw")
CLEAN_DIR = os.path.join("data", "clean")
GECKO_PATH = "C://Users//galon//AppData//Local//Programs//Python//Python310//geckodriver-v0.31.0-win64//geckodriver.exe"


def get_page(url, wait_object):

    driver = webdriver.Firefox(executable_path=GECKO_PATH)
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.XPATH, wait_object)))
    text = driver.page_source
    driver.close()
    return text

def get_table_href(text):

    soup = BeautifulSoup(text, 'html.parser')
    table_href = soup.find('iframe', {'width': '500'}).get('src')

    return pd.read_html(table_href)



if __name__ == "__main__":


    table = get_table_href(get_page("https://www.austinbike.com/index.php/austin-trail-conditions",'//iframe[@width="500"]'))













