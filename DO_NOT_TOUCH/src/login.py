
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from log_status import log_status

def login(driver, email, passwd,status_text, flag = False):
        success = True
        driver.get("https://vettersoftware.com/apps/index.php/october/login")
        if not flag:
            try:
                email_input = driver.find_element(By.NAME, 'fm_login_email')

                email_input.send_keys(email)

                password = driver.find_element(By.NAME,'fm_login_password')

                password.send_keys(passwd)

                password.send_keys(Keys.ENTER)

                time.sleep(1.5)

                success = not driver.find_element(By.NAME, 'fm_login_password').is_displayed()

            except exceptions.NoSuchElementException:
                pass


            if success:
                log_status(f"Login successful with email: {email}",status_text,)
                return True
            else:
                log_status("Incorrect credentials. Please try again.",status_text)
                return False
        else:
            return True



