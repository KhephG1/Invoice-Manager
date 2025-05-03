from invoice import Invoice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def fill_receipt(driver, invoice):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Items"))
    ).click()
    
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add Item"))
    ).click()

    flag = False
    for page in invoice.pages:
        for item in page:
            itm = driver.find_element(By.XPATH, "//input[@placeholder ='Select item (required)']")
            itm.send_keys(item.number)
            time.sleep(0.5)
            itm.send_keys(Keys.ENTER)
            time.sleep(5)
            itm = driver.find_element(By.NAME, 'receivedQuantity')
            itm.send_keys(item.quantity)
            time.sleep(5)
            itm = driver.find_element(By.NAME, 'stockQuantity')
            itm.send_keys(item.quantity)
            time.sleep(5)
            itm = driver.find_element(By.NAME, 'expiration')
            itm.send_keys(item.expiry_date)
            time.sleep(5)
            itm = driver.find_element(By.NAME, 'cost')
            itm.send_keys(item.price)
            time.sleep(5)
            itm = driver.find_element(By.NAME, 'manufacturer')
            itm.send_keys(item.manufacturer)
            time.sleep(5)
            itm = driver.find_element(By.NAME, 'lot')
            itm.send_keys(item.lot_number)
            if not flag:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "dropdown-toggle-split"))
                ).click()
                
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Save + Add"))
                ).click()
                flag=True
            else:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
                ).click()
            time.sleep(5)

    
    time.sleep(5)
