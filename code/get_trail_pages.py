from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import json, os, time, pickle

RAW_DIR = os.path.join("data", "raw")
CLEAN_DIR = os.path.join("data", "clean")

STATE_PATH = os.path.join(RAW_DIR, "state_abbs.csv")
HREF_PATH = os.path.join(RAW_DIR, "state_pages.pickle")
GECKO_PATH = "C://Users//galon//AppData//Local//Programs//Python//Python310//geckodriver-v0.31.0-win64//geckodriver.exe"


def get_pages():
    """Gets the raw html of the page showing every state"""

    url = "https://www.mtbproject.com/directory/areas"
    driver = webdriver.Firefox(executable_path=GECKO_PATH)
    driver.get(url)
    time.sleep(5)
    h = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()

    return h


def get_state_links():
    """Takes the soup and outputs the links to every state's main page"""

    soup = get_pages()
    anchors = soup.find_all("a")
    states = list(pd.read_csv(STATE_PATH)["State"].values)
    hrefs = []
    web_states = []
    for i, a in enumerate(anchors):
        try:
            if a.text.split("\n")[3] in states:
                hrefs.append(a.get("href"))
        except IndexError:
            pass
    with open(HREF_PATH, "wb") as f:
        pickle.dump(hrefs, f)

if __name__ == "__main__":

    get_state_links()
