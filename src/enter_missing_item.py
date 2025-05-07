from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

from log_status import log_status
from login import login

def navigate_func(driver):
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(((By.CLASS_NAME, "close")))
    ).click() 
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/view/inventory"]'))
    ).click()   
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "New Item"))
    ).click() 
    return


def enter_missing_item(driver,item_desc,item_num):
    """
    Opens a non-headless browser to a URL, navigates as needed, and waits for the user to close it.
    
    Args:
        target_url (str): The URL to open.
        navigate_func (function): Optional function that takes the driver and performs navigation steps.
    """

    # Navigate to target URL

    # Optional extra steps to reach a specific "window" or section of the page
    navigate_func(driver)
    itm = driver.find_element(By.XPATH, "//input[@placeholder ='Name (required)']")
    itm.send_keys(str(item_desc) + "(" + item_num + ")") 
    itm = driver.find_element(By.XPATH, "//input[@placeholder ='Display Name (optional)']")
    itm.send_keys(str(item_desc) + "(" + item_num + ")") 
    while True:
        elements = driver.find_elements(By.LINK_TEXT, "Save + Done")
        if not elements:
            break
        else:
            continue
    time.sleep(0.5)
    return
