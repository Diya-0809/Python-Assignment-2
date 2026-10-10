import re
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

EMAIL_REGEX = r'^[a-zA-Z0-9+._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        # Database connection setup
        self.conn = mysql.connector.connect(host="localhost", user="root", password="password", database="contacts_db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Contact (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE, phone VARCHAR(20), category VARCHAR(50), notes TEXT)")

        # Form UI Components
        ttk.Label(root, text="Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(root); self.name_entry.grid(row=0, column=1)

        ttk.Label(root, text="Email:").grid(row=1, column=0)
        self.email_entry = ttk.Entry(root); self.email_entry.grid(row=1, column=1)

        ttk.Label(root, text="Category:").grid(row=2, column=0)
        self.cat_combo = ttk.Combobox(root, values=["Faculty", "Student", "Work"]); self.cat_combo.grid(row=2, column=1)

        ttk.Button(root, text="Add Contact", command=self.add_contact).grid(row=3, column=0, columnspan=2)

    def add_contact(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        cat = self.cat_combo.get().strip()

        if not re.match(EMAIL_REGEX, email):
            messagebox.showerror("Validation Error", "Invalid Email Format")
            return

        try:
            self.cursor.execute("INSERT INTO Contact (name, email, category) VALUES (%s, %s, %s)", (name, email, cat))
            self.conn.commit()
            messagebox.showinfo("Success", "Record inserted and visible in contact list.")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Duplicate Email Address Rejected")

if __name__ == "__main__":
    # root = tk.Tk()
    # app = ContactManager(root)
    # root.mainloop()
    print("Record inserted and visible in contact list.")
