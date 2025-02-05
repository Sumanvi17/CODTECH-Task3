import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import json
import os

data_file = "inventory.json"

def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"users": {}, "products": {}, "sales": []}

def save_data():
    with open(data_file, "w") as f:
        json.dump(data, f)

data = load_data()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Authentication
def register_user(username, password):
    if username in data["users"]:
        return False, "User already exists!"
    hashed_pw = hash_password(password)
    data["users"][username] = hashed_pw
    save_data()
    return True, "User registered successfully!"

def login_user(username, password):
    if username not in data["users"]:
        return False, "User does not exist!"
    stored_pw = data["users"][username]
    if hash_password(password) == stored_pw:
        return True, "Login successful!"
    return False, "Incorrect password!"

# GUI Implementation
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.logged_in = False
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)

    def create_main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Inventory Management", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Add Product", command=self.add_product).pack(pady=5)
        tk.Button(self.root, text="Edit Product", command=self.edit_product).pack(pady=5)
        tk.Button(self.root, text="Remove Product", command=self.remove_product).pack(pady=5)
        tk.Button(self.root, text="View Products", command=self.view_products).pack(pady=5)
        tk.Button(self.root, text="Generate Reports", command=self.generate_reports).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = login_user(username, password)
        if success:
            self.logged_in = True
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", message)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def add_product(self):
        def save_product():
            product_id = product_id_entry.get()
            name = name_entry.get()
            quantity = quantity_entry.get()
            if not (product_id and name and quantity.isdigit()):
                messagebox.showerror("Error", "Invalid input")
                return
            data["products"][product_id] = {"name": name, "quantity": int(quantity)}
            save_data()
            messagebox.showinfo("Success", "Product added successfully!")
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Product")
        tk.Label(add_window, text="Product ID:").pack(pady=5)
        product_id_entry = tk.Entry(add_window)
        product_id_entry.pack(pady=5)
        tk.Label(add_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)
        tk.Label(add_window, text="Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack(pady=5)
        tk.Button(add_window, text="Save", command=save_product).pack(pady=10)

    def edit_product(self):
        def save_changes():
            product_id = product_id_entry.get()
            name = name_entry.get()
            quantity = quantity_entry.get()
            if product_id not in data["products"]:
                messagebox.showerror("Error", "Product not found!")
                return
            if not (name and quantity.isdigit()):
                messagebox.showerror("Error", "Invalid input!")
                return
            data["products"][product_id]["name"] = name
            data["products"][product_id]["quantity"] = int(quantity)
            save_data()
            messagebox.showinfo("Success", "Product updated successfully!")
            edit_window.destroy()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Product")
        tk.Label(edit_window, text="Product ID:").pack(pady=5)
        product_id_entry = tk.Entry(edit_window)
        product_id_entry.pack(pady=5)
        tk.Label(edit_window, text="New Name:").pack(pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.pack(pady=5)
        tk.Label(edit_window, text="New Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.pack(pady=5)
        tk.Button(edit_window, text="Save", command=save_changes).pack(pady=10)

    def remove_product(self):
        def delete_product():
            product_id = product_id_entry.get()
            if product_id not in data["products"]:
                messagebox.showerror("Error", "Product not found!")
                return
            del data["products"][product_id]
            save_data()
            messagebox.showinfo("Success", "Product removed successfully!")
            remove_window.destroy()

        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Product")
        tk.Label(remove_window, text="Product ID:").pack(pady=5)
        product_id_entry = tk.Entry(remove_window)
        product_id_entry.pack(pady=5)
        tk.Button(remove_window, text="Delete", command=delete_product).pack(pady=10)

    def view_products(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("Products")
        tree = ttk.Treeview(view_window, columns=("ID", "Name", "Quantity"), show="headings")
        tree.heading("ID", text="Product ID")
        tree.heading("Name", text="Name")
        tree.heading("Quantity", text="Quantity")
        for pid, pdata in data["products"].items():
            tree.insert("", "end", values=(pid, pdata["name"], pdata["quantity"]))
        tree.pack(fill=tk.BOTH, expand=True)

    def generate_reports(self):
        def generate_low_stock():
            threshold = threshold_entry.get()
            if not threshold.isdigit():
                messagebox.showerror("Error", "Invalid threshold!")
                return
            threshold = int(threshold)
            report = [f"ID: {pid}, Name: {pdata['name']}, Quantity: {pdata['quantity']}" 
                      for pid, pdata in data["products"].items() if pdata["quantity"] < threshold]
            messagebox.showinfo("Low-Stock Report", "\n".join(report) if report else "No low-stock products.")

        report_window = tk.Toplevel(self.root)
        report_window.title("Generate Reports")
        tk.Label(report_window, text="Low-Stock Threshold:").pack(pady=5)
        threshold_entry = tk.Entry(report_window)
        threshold_entry.pack(pady=5)
        tk.Button(report_window, text="Generate Low-Stock Report", command=generate_low_stock).pack(pady=10)

    def logout(self):
        self.logged_in = False
        self.create_login_screen()

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()



