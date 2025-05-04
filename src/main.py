from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from invoice import Invoice
from login import login
from make_receipt import make_receipt
from fill_receipt import fill_receipt
from post_receipt import post_the_receipt

options  = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
driver.implicitly_wait(2)

def main():
    inv = Invoice("test2.pdf")
    inv.parse()
    print(inv)
    login(driver)
    make_receipt(driver, inv)
    fill_receipt(driver, inv)
    post_the_receipt(driver)

if __name__ == "__main__":
    main()