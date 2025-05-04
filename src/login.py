
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from log_status import log_status

def login(driver, email, passwd,name, status_text, Flag=False):

    driver.get("https://vettersoftware.com/apps/index.php/october/login")

    if not Flag:
        email_input = driver.find_element(By.NAME, 'fm_login_email')

        email_input.send_keys(email)

        password = driver.find_element(By.NAME,'fm_login_password')

        password.send_keys(passwd)

        

        password.send_keys(Keys.ENTER)

        log_status(f"Login successful with email: {email}",status_text,)
    else:
        the_name = None
        while True:
            try:
                the_name = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@class="vs__search" and @type="search"]'))
                )
                break
            except exceptions.ElementNotInteractableException:
                pass
        the_name.send_keys(name)
        time.sleep(10)
        the_name.send_keys(Keys.ENTER)
        time.sleep(10)
        p_word = driver.find_element(By.XPATH, '//input[@name="password"]')
        p_word.send_keys(passwd)
        WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/view/inventory"]'))
        )

    return driver


