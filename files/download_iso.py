from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.webdriver.chrome.options import Options
def make_driver():
    """Create a Chrome WebDriver using Selenium Manager (no manual driver path)."""
    options = Options()
    options.add_argument("--headless=new")  # optional: run without opening Chrome window
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400,1000)
    return driver

def download_isochrone():
    """
    downloads isochrone files used for constant mass curves in pltUBVRI.py
    """

    print("------------------------------------- Download Isochrone Data -------------------------------------")
    print("What Isochrone track would you like to download: ")
    print("A: v/vcrit = 0.4 ")
    print("B: v/vcrit = 0.0 ")

    # display options for v/vcrit
    user_input1 = input("Select A or B (case sensitive). ")
    while user_input1 not in ("A", "B"):
        print("Not a valid input please select A or B.")
        user_input1 = input("Select A or B (case sensitive). ")

    driver = make_driver()
    try:
        driver.get("http://waps.cfa.harvard.edu/MIST/model_grids.html")
        xpath = '//*[@id="content"]/article/p[19]/a' if user_input1 == "A" else '//*[@id="content"]/article/p[43]/a'
        driver.find_element(By.XPATH, xpath).click()
        print("Isochrone link clicked; check your browser/downloads settings.")
    finally:
        driver.quit()
    #driver.find_element_by_link_text("UBV(RI)c + 2MASS JHKs + Kepler + Hipparcos + Tycho + Gaia (116MB)").click()
 
#download_isochrone()