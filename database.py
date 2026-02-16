import sqlite3

def init_db():
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Tworzymy tabelę departments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Tworzymy tabelę employees
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        salary REAL NOT NULL,
        department_id INTEGER NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    """)

    # Sprawdzamy, czy tabela departments jest pusta
    cursor.execute("SELECT COUNT(*) FROM departments")
    count = cursor.fetchone()[0]

    if count == 0:
        # Wstawiamy domyślne działy
        default_departments = [("IT",), ("HR",), ("Sales",), ("Finance",)]
        cursor.executemany("INSERT INTO departments (name) VALUES (?)", default_departments)
        print("Dodano domyślne działy do bazy.")

    connection.commit()
    connection.close()
    print("Baza danych została zainicjalizowana ✅")

# Jeśli uruchomimy ten plik bezpośrednio
if __name__ == "__main__":
    init_db()
