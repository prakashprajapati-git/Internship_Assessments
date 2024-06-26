import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prakash's Password Generator")
        self.geometry("400x400")
        self.configure(bg='#1E1E1E')
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Password Generator", font=("Helvetica", 18, 'bold'), bg='#1E1E1E', fg='#FFFFFF')
        title_label.pack(pady=20)

        length_frame = tk.Frame(self, bg='#1E1E1E')
        length_frame.pack(pady=10)

        length_label = tk.Label(length_frame, text="Password Length:", font=("Helvetica", 14), bg='#1E1E1E', fg='#FFFFFF')
        length_label.pack(side=tk.LEFT, padx=5)

        self.length_var = tk.IntVar(value=8)
        length_spinbox = tk.Spinbox(length_frame, from_=8, to_=32, textvariable=self.length_var, font=("Helvetica", 14), width=5, bg='#3A3A3A', fg='#FFFFFF', bd=0, highlightthickness=0)
        length_spinbox.pack(side=tk.LEFT, padx=5)

        generate_button = tk.Button(self, text="Generate Password", font=("Helvetica", 14), bg='#1E90FF', fg='#FFFFFF', bd=0, highlightthickness=0, command=self.generate_password)
        generate_button.pack(pady=20)

        self.password_entry = tk.Entry(self, font=("Helvetica", 14), width=24, bd=0, bg="#3A3A3A", fg="#FFFFFF", justify=tk.CENTER)
        self.password_entry.pack(pady=10)

        copy_button = tk.Button(self, text="Copy to Clipboard", font=("Helvetica", 14), bg='#FFA500', fg='#FFFFFF', bd=0, highlightthickness=0, command=self.copy_to_clipboard)
        copy_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 12), bg='#1E1E1E', fg='#00FF00')
        self.result_label.pack(pady=5)

    def generate_password(self):
        length = self.length_var.get()
        if length < 8 or length > 32:
            messagebox.showerror("Error", "Password length must be between 8 and 32")
            return
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo("Info", "Password copied to clipboard")
        self.result_label.config(text="Password copied to clipboard")

if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()
