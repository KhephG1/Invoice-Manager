from invoice import Invoice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from log_status import log_status
import time

def post_the_receipt(driver, status_text):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Post Receipt"))
    ).click()
    
    WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary"))
    ).click()

    log_status("Receipt posted ! Please check Daysmart to verify. (drag another pdf) OR (click 'Exit')", status_text)



