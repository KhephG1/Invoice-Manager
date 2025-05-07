import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import ttk, messagebox

def log_status(message, status_text):
    status_text.insert(tk.END, message + "\n")
    status_text.yview(tk.END)