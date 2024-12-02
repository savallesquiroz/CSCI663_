import tkinter as tk
from tkinter import scrolledtext, messagebox

class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Project GUI")
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50")  # Fondo oscuro

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
            root, state='disabled', height=10, bg="#34495E", fg="#ECF0F1", font=("Courier", 10), wrap=tk.WORD
        )
        self.message_area.pack(padx=10, pady=5, fill="both")

        # Input text for messages
        self.input_label = tk.Label(
            root, text="Enter your message:", font=("Helvetica", 12), fg="#ECF0F1", bg="#2C3E50"
        )
        self.input_label.pack(anchor="w", padx=10)
        self.message_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1")
        self.message_entry.pack(padx=10, pady=5)

        # Buttons Frame
        self.button_frame = tk.Frame(root, bg="#2C3E50")
        self.button_frame.pack(pady=10)

        self.encrypt_button = tk.Button(
            self.button_frame, text="Encrypt", command=self.encrypt_message,
            bg="#1ABC9C", fg="#ECF0F1", font=("Helvetica", 12), width=12
        )
        self.encrypt_button.grid(row=0, column=0, padx=5)

        self.decrypt_button = tk.Button(
            self.button_frame, text="Decrypt", command=self.decrypt_message,
            bg="#E74C3C", fg="#ECF0F1", font=("Helvetica", 12), width=12
        )
        self.decrypt_button.grid(row=0, column=1, padx=5)

    def encrypt_message(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message.")
            return
        encrypted_message = f"ENCRYPTED({message})"  # Simulated encryption
        self.message_area.config(state='normal')
        self.message_area.insert(tk.END, f"Encrypted: {encrypted_message}\n")
        self.message_area.config(state='disabled')
        self.message_entry.delete(0, tk.END)

    def decrypt_message(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message.")
            return
        decrypted_message = f"DECRYPTED({message})"  # Simulated decryption
        self.message_area.config(state='normal')
        self.message_area.insert(tk.END, f"Decrypted: {decrypted_message}\n")
        self.message_area.config(state='disabled')
        self.message_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()
