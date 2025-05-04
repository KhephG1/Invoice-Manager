from invoice import Invoice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def make_receipt(driver, invoice, status_text):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/view/inventory"]'))
    ).click()
    
    
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Receipts"))
    ).click()
    
    
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "New Receipt"))
    ).click()
    
    

    supplier = driver.find_element(By.XPATH, "//input[@placeholder ='Select Supplier (required)']")

    supplier.send_keys("Western Drug Distribution Centre")
    supplier.send_keys(Keys.ENTER)

   

    invoice_number = driver.find_element(By.NAME, 'invoice')

    invoice_number.send_keys(invoice.invoice_number)

    

    WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary"))
    ).click()

    