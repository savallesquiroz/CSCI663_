import sys
import queue
import tkinter as tk
from tkinter import scrolledtext, messagebox

class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Project GUI")
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")  # Fondo oscuro
        self.root.bind("<Return>", lambda event: self.send_encryption_message())

        # Title Label
        self.title_label = tk.Label(
            root, text="Crypto Project", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#2C3E50"
        )
        self.title_label.pack(pady=10)

        # Message display area
        self.message_label = tk.Label(
            root, text="Messages:", font=("Helvetica", 12, "bold"), fg="#ECF0F1", bg="#2C3E50"
        )
        self.message_label.pack(anchor="w", padx=10)
        self.message_area = scrolledtext.ScrolledText(
            root, state='disabled', height=10, bg="#34495E", fg="#ECF0F1", font=("Courier", 12), wrap=tk.WORD
        )
        self.message_area.pack(padx=10, pady=5, fill="both")

        # Message Queue
        self.message_queue = queue.Queue()

        # Buttons Frame
        self.button_frame = tk.Frame(root, bg="#2C3E50")
        self.button_frame.pack(pady=10)

        if sys.argv[1] == "client":
            # Input text for messages
            self.input_label = tk.Label(
                root, text="Enter your message:", font=("Helvetica", 12), fg="#ECF0F1", bg="#2C3E50"
            )
            self.input_label.pack(anchor="center", padx=10)
            self.message_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1")
            self.message_entry.pack(padx=10, pady=5)
            self.instructions_label = tk.Label(
                root, text="Press <Enter> to send the message.", font=("Helvetica", 12), fg="#ECF0F1", bg="#2C3E50"
            )
            self.instructions_label.pack(anchor="center", padx=10)

    def send_message(self, message):
        if not message:
            messagebox.showwarning("Warning", "Please enter a message.")
            return
        self.message_area.config(state='normal')
        self.message_area.insert(tk.END, f"{message}\n")
        self.message_area.config(state='disabled')
        if sys.argv[1] == "client":
            self.message_entry.delete(0, tk.END)

    def send_encryption_message(self):
        message = self.message_entry.get() if self.message_entry.get() else None
        self.message_queue.put(message)
        self.message_entry.delete(0, tk.END)
