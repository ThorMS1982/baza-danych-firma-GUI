import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# -----------------------------
# Funkcja pobierająca działy z bazy
# -----------------------------
def get_departments():
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM departments")
    departments = [row[0] for row in cursor.fetchall()]

    connection.close()
    return departments


# -----------------------------
# Funkcja dodająca pracownika
# -----------------------------
def add_employee():
    name = entry_name.get()
    email = entry_email.get()
    salary = entry_salary.get()
    department = department_var.get()

    if not name or not email or not salary or not department:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
        return

    try:
        salary = float(salary)
    except ValueError:
        messagebox.showerror("Błąd", "Wynagrodzenie musi być liczbą.")
        return

    try:
        connection = sqlite3.connect("company.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM departments WHERE name = ?", (department,))
        department_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO employees (name, email, salary, department_id)
            VALUES (?, ?, ?, ?)
        """, (name, email, salary, department_id))

        connection.commit()
        connection.close()

        messagebox.showinfo("Sukces", "Pracownik został dodany.")

        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_salary.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror("Błąd", "Email już istnieje w bazie.")


# -----------------------------
# Główne okno aplikacji
# -----------------------------
root = tk.Tk()
root.title("System zarządzania pracownikami")
root.geometry("400x300")

# Imię
tk.Label(root, text="Imię i nazwisko").pack(pady=5)
entry_name = tk.Entry(root, width=40)
entry_name.pack()

# Email
tk.Label(root, text="Email").pack(pady=5)
entry_email = tk.Entry(root, width=40)
entry_email.pack()

# Wynagrodzenie
tk.Label(root, text="Wynagrodzenie").pack(pady=5)
entry_salary = tk.Entry(root, width=40)
entry_salary.pack()

# Dział (lista rozwijana)
tk.Label(root, text="Dział").pack(pady=5)

department_var = tk.StringVar()
departments = get_departments()

department_dropdown = ttk.Combobox(
    root,
    textvariable=department_var,
    values=departments,
    state="readonly"
)
department_dropdown.pack()

# Przycisk
tk.Button(root, text="Dodaj pracownika", command=add_employee).pack(pady=20)

root.mainloop()
