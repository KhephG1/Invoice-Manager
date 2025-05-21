import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk, messagebox
from log_status import log_status
from enum import Enum
import pickle
import os
import sys
from invoice import Invoice
from login import login
from make_receipt import make_receipt
from fill_receipt import fill_receipt
from enter_qty import enter_quantity
from post_receipt import post_the_receipt

# Setup WebDriver
options = Options()
options.add_argument("--window-size=1920,1080")
#options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(2)


class states(Enum):
    DROP = 1
    LOGIN = 2
    FILL = 3
    ENTER = 4
    POST = 5

state = states.LOGIN

class Manager_FSM:
    def __init__(self, root):

        self.quantities = {}
        self.invoice = None
        self.status_text = None
        self.state = states.DROP
        self.email = None
        self.password = None
        self.root = root
        self.txt_path = None
        self.top_frame = None
        self.middle_frame = None
        self.drop_area = None
        self.log_frame = None
        self.scrollbar = None
        self.bottom_frame = None
        self.t = None

        self.determine_qty_filepath()
        self.populate_qty()

        self.init_window()
        self.init_buttons()

    def determine_qty_filepath(self):
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle
            base_path = os.path.dirname(sys.executable)
        else:
            # If the application is run in a normal Python environment
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Define the path for the text file
        txt_path = (str)(base_path).split(os.sep)
        self.txt_path = os.sep.join(txt_path) + "\DO_NOT_TOUCH\quantities.csv"
        print(self.txt_path)

    def populate_qty(self):
        if os.path.exists(self.txt_path) and os.path.getsize(self.txt_path) > 0:
            with open(self.txt_path) as f:
                reader = csv.reader(f)
                header_row = next(reader)
                for row in reader:
                    self.quantities[row[0]] = int(row[1])
                print(self.quantities)

        else:
            pass

    def init_window(self):

        self.root.title("Invoice Receiver")
        self.root.iconbitmap("DO_NOT_TOUCH/assiniboia.ico")
        self.root.geometry('1200x800')

        # --- Top Frame ---
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(self.top_frame, text="Welcome to Invoice Receiver", font=("Segoe UI", 16)).pack()

        # --- Middle Frame (DnD and Log Side-by-Side) ---
        self.middle_frame = ttk.Frame(self.root)
        self.middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Drag and Drop area
        self.drop_area = ttk.Label(
            self.middle_frame,
            text="1. Drop your invoice here",
            background="#e0e0e0",
            relief="ridge",
            anchor="center",
            font=("Segoe UI", 12),
            width=60
        )
        self.drop_area.pack(side="left", fill="both", expand=True, padx=(0, 10), ipadx=20, ipady=100)
        self.drop_area.drop_target_register(DND_FILES)

        # Text area with self.scrollbar
        self.log_frame = ttk.Frame(self.middle_frame)
        self.log_frame.pack(side="right", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.log_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.status_text = tk.Text(self.log_frame, wrap="word", font=("Segoe UI", 10),
                                   yscrollcommand=self.scrollbar.set)
        self.status_text.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.status_text.yview)

        # Bind drop event
        self.drop_area.dnd_bind('<<Drop>>', lambda event: self.to_drop_state(event))

    def init_buttons(self):
        # --- Bottom Frame (Buttons) ---
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(self.bottom_frame, text="Post", command=lambda: self.to_post_state()).pack(side="left", padx=10)
        ttk.Button(self.bottom_frame, text="Exit", command=lambda: self.quit_program()).pack(side="right", padx=10)



    def to_drop_state(self,event):
        if self.state == states.DROP:
            file_path = event.data.strip('{}')
            if file_path.lower().endswith(".pdf"):
                self.invoice = Invoice(file_path)
                log_status(f"PDF received with path: {file_path}", self.status_text, )
                self.invoice.parse(self.status_text)
                self.to_login_state()
            else:
                messagebox.showerror("Invalid File :(")

    def to_login_state(self):

        def submit_credentials():
            success = False
            self.email = email_var.get()
            self.password = password_var.get()
            success = login(driver, str(self.email), str(self.password),self.status_text)

            if success:
                login_window.destroy()
                self.to_fill_state()
            else:
                messagebox.showerror("Invalid Credentials")


        if self.state == states.DROP and self.email is not None and self.password is not None :
            print("Here")
            login(driver, str(self.email), str(self.password), self.status_text, True)
            self.state = states.LOGIN
            self.to_fill_state()
        else:
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
            self.state = states.LOGIN


    def to_fill_state(self):
        global driver
        make_receipt(driver, self.invoice, self.status_text)
        fill_receipt(driver, self.invoice, self.status_text)
        self.state = states.FILL
        self.to_enter_state()

    def check_thread_done(self):

        if self.t.is_alive():
            self.root.after(100, self.check_thread_done)  # check again in 100ms
        else:
           pass
    def to_enter_state(self):
        global driver

        self.t = threading.Thread(target=enter_quantity, args=(driver, self.invoice, self.status_text, self.root, self.quantities))
        self.t.start()
        self.root.after(100, self.check_thread_done)

        self.state = states.ENTER

    def to_post_state(self):
        if self.state == states.ENTER:
            self.state = states.POST
            print("posting receipt")
            post_the_receipt(driver, self.status_text)
            self.state = states.DROP
        else:
            print(self.state)
            pass #remain in the current state (whatever it is)

    def quit_program(self):
        self.root.quit()
        with open(self.txt_path, 'w', newline='') as f:
            header_row = ['item_number', 'quantities']
            writer = csv.writer(f)
            writer.writerow(header_row)
            print(self.quantities)
            writer.writerows(self.quantities.items())



def main():
    root = TkinterDnD.Tk()
    app = Manager_FSM(root)
    root.mainloop()



if __name__ == "__main__":
    main()

