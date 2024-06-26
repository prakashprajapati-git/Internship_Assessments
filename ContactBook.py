import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        # Create database connection
        self.conn = sqlite3.connect("contacts.db")
        self.cur = self.conn.cursor()
        self.create_table()

        # Create styles
        self.create_styles()

        # Create GUI elements
        self.create_gui()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (id INTEGER PRIMARY KEY,
                             name TEXT,
                             phone TEXT,
                             email TEXT,
                             address TEXT)''')
        self.conn.commit()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure colors
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Configure button styles
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.map("TButton",
                  foreground=[('pressed', 'white'), ('active', 'black')],
                  background=[('pressed', '!disabled', '#3d84b8'), ('active', '#78c0e0')])

    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Left frame for input fields and buttons
        left_frame = ttk.Frame(main_frame, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input fields
        ttk.Label(left_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(left_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(left_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(left_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(left_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(left_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(left_frame, text="Address:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(left_frame, width=30)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(left_frame, padding="10")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Contact", command=self.add_contact, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Contact", command=self.update_contact, style="TButton").grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact, style="TButton").grid(row=0, column=2, padx=5)

        # Search field
        search_frame = ttk.Frame(left_frame, padding="10")
        search_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_contact, style="TButton").grid(row=0, column=2, padx=5)

        # Right frame for contact list
        right_frame = ttk.Frame(main_frame, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Treeview for contact list
        self.tree = ttk.Treeview(right_frame, columns=("Name", "Phone"), show="headings", height=15)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.column("Name", width=200)
        self.tree.column("Phone", width=150)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind treeview selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        # Populate the treeview
        self.view_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.cur.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                             (name, phone, email, address))
            self.conn.commit()
            self.clear_entries()
            self.view_contacts()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showerror("Error", "Name and Phone are required fields!")

    def view_contacts(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT name, phone FROM contacts")
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)

    def search_contact(self):
        search_term = self.search_entry.get()
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                         ('%' + search_term + '%', '%' + search_term + '%'))
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)

    def update_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            address = self.address_entry.get()

            if name and phone:
                self.cur.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE name=?",
                                 (name, phone, email, address, self.tree.item(selected_item)['values'][0]))
                self.conn.commit()
                self.clear_entries()
                self.view_contacts()
                messagebox.showinfo("Success", "Contact updated successfully!")
            else:
                messagebox.showerror("Error", "Name and Phone are required fields!")
        else:
            messagebox.showerror("Error", "Please select a contact to update!")

    def delete_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
                self.cur.execute("DELETE FROM contacts WHERE name=?", (self.tree.item(selected_item)['values'][0],))
                self.conn.commit()
                self.clear_entries()
                self.view_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select a contact to delete!")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            name = self.tree.item(selected_item)['values'][0]
            self.cur.execute("SELECT * FROM contacts WHERE name=?", (name,))
            contact = self.cur.fetchone()
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact[1])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact[2])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact[3])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, contact[4])

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()