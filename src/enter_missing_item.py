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

def navigate_func(driver, email, password,name, status_text):
    login(driver, email, password,name, status_text)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/view/inventory"]'))
    ).click()   

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "New Item"))
    ).click() 
    print("Here1")
    return


def enter_missing_item(email, password, status_text,root):
    """
    Opens a non-headless browser to a URL, navigates as needed, and waits for the user to close it.
    
    Args:
        target_url (str): The URL to open.
        navigate_func (function): Optional function that takes the driver and performs navigation steps.
    """

    # Open a non-headless Chrome browser
    options = Options()
    # optionally add any flags here
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # Navigate to target URL

    # Optional extra steps to reach a specific "window" or section of the page
    navigate_func(driver, email, password,"", status_text)
    print("Here2")
    # Monitor the browser until the user closes it
    def monitor_browser():
        try:

            _ = driver.title  # Will raise if browser is closed
            root.after(1000, monitor_browser)
        except WebDriverException:
            log_status("Thanks!", status_text)
            
            time.sleep(1)
    print("Here3")
    log_status("Waiting for you to enter item in inventory...", status_text)
    root.after(1000, monitor_browser)
    print("Here 4")
    return
