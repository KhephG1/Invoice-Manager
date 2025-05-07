from invoice import Invoice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from log_status import log_status
import threading
import tkinter as tk
from tkinter import ttk

def prompt_user_input(invoice_item,user_input_event, user_input_value,root,quantities):
    prompt = tk.Toplevel(root)
    prompt.title("Additional Information")
    prompt.geometry("800x200")

    ttk.Label(prompt, text= f"Please enter the number of {invoice_item.type} for a single order of {invoice_item.description}:", font=("Segoe UI", 11)).pack(pady=(20, 10))

    user_input = tk.StringVar()
    entry = ttk.Entry(prompt, textvariable=user_input, width=50)
    entry.pack(pady=(0, 20))
    entry.focus()

    def submit():
        input = user_input.get()
        quantities.update({invoice_item.number : int(input)})
        user_input_value.append(input)
        user_input_event.set()
        prompt.destroy()

    ttk.Button(prompt, text="Submit", command=submit).pack()


def enter_quantity(driver, invoice, status_text,root, quantities):
    time.sleep(0.3)
    i=0
    for page in invoice.pages:
        for item in page:
            time.sleep(0.3)
            icons = driver.find_elements(By.CLASS_NAME, "cus-cog-down")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(icons[i])
            ).click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Edit Item"))
            ).click()
            input_val = None
            if item.number in quantities:
                input_val = quantities[item.number]
            else:
                user_input_event = threading.Event()
                user_input_value = []

                root.after(0, prompt_user_input, item,user_input_event, user_input_value, root,quantities)
                
                user_input_event.wait()
                input_val = user_input_value[0]

            itm = driver.find_element(By.NAME, 'receivedQuantity')
            itm.clear()
            itm.send_keys(str(int(input_val) * int(item.quantity)))
            time.sleep(0.3)
            itm2 = driver.find_element(By.NAME, 'stockQuantity')
            itm2.clear()
            itm2.send_keys(str(int(input_val) * int(item.quantity)))
            
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
            ).click()

            log_status(f"Quantity: {int(input_val) * int(item.quantity)} assigned to {item.description}",status_text)

            time.sleep(0.3)
            i += 1
    log_status("Complete! Click 'Post' to post the receipt in Daysmart",status_text)
    
    