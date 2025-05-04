from invoice import Invoice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time



def promp_user_for_quantity(type,quantity,description):
    print(type, quantity, description)
    
def fill_receipt(driver, invoice):
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
            itm = driver.find_element(By.XPATH, "//input[@placeholder ='Select item (required)']")
            itm.send_keys(item.number)
            time.sleep(0.5)
            itm.send_keys(Keys.ENTER)
            
            itm = driver.find_element(By.NAME, 'receivedQuantity')
            type = driver.find_element(By.CSS_SELECTOR, "div.quantity span")
            promp_user_for_quantity(type.text, item.quantity, item.description)
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
            

    
   
