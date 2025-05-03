from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time



options  = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
driver.implicitly_wait(2)
driver.get("https://vettersoftware.com/apps/index.php/october/login")

email_input = driver.find_element(By.NAME, 'fm_login_email')

email_input.send_keys("Bill.kuzyk@gmail.com")

password = driver.find_element(By.NAME,'fm_login_password')

password.send_keys("51Grimston")

time.sleep(4)

password.send_keys(Keys.ENTER)

time.sleep(4)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/view/inventory"]'))
).click()

time.sleep(4)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Receipts"))
).click()

time.sleep(5)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "New Receipt"))
).click()

time.sleep(5)
