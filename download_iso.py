from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
'done'
s = Service("/usr/local/bin/chromedriver")
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
    while user_input1 != "B" and user_input1 != "A":
        print("Not a valid input please select A or B.")
        user_input1 = input("Select A or B (case sensitive). ")

    driver = webdriver.Chrome(service=s)
    driver.get("http://waps.cfa.harvard.edu/MIST/model_grids.html")
    driver.maximize_window()
    if user_input1 == "A":
        driver.find_element_by_xpath('//*[@id="content"]/article/p[19]/a').click()
    else:
        driver.find_element_by_xpath('//*[@id="content"]/article/p[43]/a').click()

    
    #driver.find_element_by_link_text("UBV(RI)c + 2MASS JHKs + Kepler + Hipparcos + Tycho + Gaia (116MB)").click()
 
#download_isochrone()