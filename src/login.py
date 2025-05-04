
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from log_status import log_status

def login(driver, email, passwd, status_text):

    driver.get("https://vettersoftware.com/apps/index.php/october/login")

    email_input = driver.find_element(By.NAME, 'fm_login_email')

    email_input.send_keys(email)

    password = driver.find_element(By.NAME,'fm_login_password')

    password.send_keys(passwd)

    

    password.send_keys(Keys.ENTER)

    log_status(f"Login successful with email: {email}",status_text,)
    
    return driver


