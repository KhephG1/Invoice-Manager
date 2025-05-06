from invoice import Invoice
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from log_status import log_status
from enter_qty import enter_quantity
import threading
from login import login

from enter_missing_item import enter_missing_item

def populate(driver,item):
    itm = driver.find_element(By.XPATH, "//input[@placeholder ='Select item (required)']")
    itm.send_keys(item.number)
    time.sleep(0.5)
    itm.send_keys(Keys.ENTER)
    
    itm = driver.find_element(By.NAME, 'receivedQuantity')
    type = driver.find_element(By.CSS_SELECTOR, "div.quantity span")
    item.type = type.text
    itm.send_keys(item.quantity)
    itm = driver.find_element(By.NAME, 'stockQuantity')
    itm.send_keys(item.quantity)
    
    itm = driver.find_element(By.NAME, 'expiration')
    itm.send_keys(item.expiry_date)
    
    itm = driver.find_element(By.NAME, 'cost')
    itm.send_keys(item.price)
    
    itm = driver.find_element(By.NAME, 'manufacturer')
    itm.send_keys(item.manufacturer)
    
    itm = driver.find_element(By.NAME, 'lot')
    itm.send_keys(item.lot_number)
    
def fill_receipt(driver, invoice, status_text):
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Items"))
    ).click()
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add Item"))
    ).click()

    flag = False
    for page in invoice.pages:
        for item in page:
            try:
                if not flag:
                    populate(driver,item)
                    WebDriverWait(driver, 4).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-toggle-split"))
                    )
                    WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "dropdown-toggle-split"))
                    ).click()
                    
                    WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Save + Add"))
                    ).click()
                    flag=True
                    
                else:
                    populate(driver,item)
                    WebDriverWait(driver, 4).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-toggle-split"))
                    )
                    WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
                    ).click()
            except exceptions.TimeoutException:
                time.sleep(0.5)
                enter_missing_item(driver,item.description,item.number)
                time.sleep(0.5)
                while True:
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/view/inventory"]'))
                        ).click()
                        break
                    except exceptions.ElementClickInterceptedException:
                        pass
                WebDriverWait(driver, 10000).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Receipts"))
                ).click()
                WebDriverWait(driver, 10000).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "View All Receipts"))
                ).click()
                time.sleep(0.5)
                WebDriverWait(driver, 10000).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, f"Receipt #{invoice.receipt_num}"))
                ).click()
                time.sleep(0.5)
                WebDriverWait(driver, 10000).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Items"))
                ).click()
                time.sleep(0.5)
                WebDriverWait(driver, 10000).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Add Item"))
                ).click()
                populate(driver,item)
                WebDriverWait(driver, 1000).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "dropdown-toggle-split"))
                ).click()
                WebDriverWait(driver,1000).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Save + Add"))
                ).click()
                flag=True


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "close"))
        ).click()   
    log_status("Receipt Filled Successfully. Note: Press 'Enter Quantities' to ensure item quantities are correct", status_text)
            
            

    
   
