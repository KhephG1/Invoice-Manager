from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk, messagebox
from log_status import log_status

from invoice import Invoice
from login import login
from make_receipt import make_receipt
from fill_receipt import fill_receipt
from enter_qty import enter_quantity
from post_receipt import post_the_receipt
invoice = None

root = TkinterDnD.Tk()

def open_login_window(status_text):
    def submit_credentials():
        email = email_var.get()
        password = password_var.get()
        login(driver, str(email), str(password), status_text)
        login_window.destroy()

    login_window = tk.Toplevel()
    login_window.title("Daysmart Login")
    login_window.geometry("300x200")
    ttk.Label(login_window, text = "Email:").pack(pady=(10,0))
    email_var = tk.StringVar()
    ttk.Entry(login_window, textvariable=email_var).pack(pady=5)

    ttk.Label(login_window, text="Daysmart Password:").pack(pady=(10, 0))
    password_var = tk.StringVar()
    ttk.Entry(login_window, textvariable=password_var, show="*").pack(pady=5)

    ttk.Button(login_window, text="Submit", command=submit_credentials).pack(pady=20)

def receipt(status_text):
    global invoice
    make_receipt(driver,invoice, status_text)

def fill(status_text):
    global invoice, root
    fill_receipt(driver, invoice, status_text, root)

def enter(status_text):
    global invoice,root
    threading.Thread(target=enter_quantity, args=(driver, invoice, status_text, root)).start()

def post(status_text):
    global invoice
    post_the_receipt(driver, status_text)

def handle_file_drop(event, status_text):
    global invoice, root
    file_path = event.data.strip('{}')
    if file_path.lower().endswith(".pdf"):
        invoice = Invoice(file_path)
        log_status(f"PDF received with path: {file_path}",status_text,)
        
    else:
        messagebox.showerror("Invalid File :(")


# Setup WebDriver
options = Options()
options.add_argument("--window-size=1920,1080")
#options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(2)

def main():
    root.title("Invoice Receiver")
    root.iconbitmap("assiniboia.ico")
    root.geometry('1200x800')

    # --- Top Frame ---
    top_frame = ttk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=10)
    ttk.Label(top_frame, text="Welcome to Invoice Receiver", font=("Segoe UI", 16)).pack()

    # --- Middle Frame (DnD and Log Side-by-Side) ---
    middle_frame = ttk.Frame(root)
    middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Drag and Drop area
    drop_area = ttk.Label(
        middle_frame,
        text="1. Drop your invoice here",
        background="#e0e0e0",
        relief="ridge",
        anchor="center",
        font=("Segoe UI", 12),
        width=60
    )
    drop_area.pack(side="left", fill="both", expand=True, padx=(0, 10), ipadx=20, ipady=100)
    drop_area.drop_target_register(DND_FILES)

    # Text area with scrollbar
    log_frame = ttk.Frame(middle_frame)
    log_frame.pack(side="right", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(log_frame)
    scrollbar.pack(side="right", fill="y")

    status_text = tk.Text(log_frame, wrap="word", font=("Segoe UI", 10), yscrollcommand=scrollbar.set)
    status_text.pack(fill="both", expand=True)
    scrollbar.config(command=status_text.yview)

    # Bind drop event
    drop_area.dnd_bind('<<Drop>>', lambda event: handle_file_drop(event, status_text))

    # --- Bottom Frame (Buttons) ---
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(fill="x", padx=10, pady=10)
    ttk.Button(bottom_frame, text="2. Login", command=lambda: open_login_window(status_text)).pack(side="left", padx=10)
    ttk.Button(bottom_frame, text="3. Process Invoice", command=lambda: invoice.parse(status_text)).pack(side="left", padx=10)
    ttk.Button(bottom_frame, text="4. Make Receipt", command=lambda: receipt(status_text)).pack(side="left", padx=10)
    ttk.Button(bottom_frame, text="Exit", command=root.quit).pack(side="right", padx=10)
    ttk.Button(bottom_frame, text = "5. Fill Receipt", command=lambda: fill(status_text)).pack(side = "left", padx=10)
    ttk.Button(bottom_frame, text = "6. Enter Quantities", command=lambda: enter(status_text)).pack(side = "left", padx=10)
    ttk.Button(bottom_frame, text = "7. Post", command=lambda: post(status_text)).pack(side = "left", padx=10)
    root.mainloop()

if __name__ == "__main__":
    main()

    # all widgets will be here
    # Execute Tkinter

    # inv = Invoice("test2.pdf")
    # inv.parse()
    # print(inv)
    # login(driver)
    # make_receipt(driver, inv)
    # fill_receipt(driver, inv)
    # post_the_receipt(driver)

