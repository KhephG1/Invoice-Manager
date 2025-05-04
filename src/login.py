
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login(driver):

    driver.get("https://vettersoftware.com/apps/index.php/october/login")

    email_input = driver.find_element(By.NAME, 'fm_login_email')

    email_input.send_keys("Bill.kuzyk@gmail.com")

    password = driver.find_element(By.NAME,'fm_login_password')

    password.send_keys("51Grimston")

    

    password.send_keys(Keys.ENTER)

    
    return driver


