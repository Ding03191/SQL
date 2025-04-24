import sqlite3
import datetime

DB_NAME = 'bookstore.db'


def connect_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            book_title TEXT NOT NULL,
            unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_sale():
    try:
        date = input("Enter date (YYYY-MM-DD): ")
        datetime.datetime.strptime(date, '%Y-%m-%d')
        title = input("Enter book title: ")
        unit_price = float(input("Enter unit price: "))
        quantity = int(input("Enter quantity sold: "))

        conn = connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO sales (date, book_title, unit_price, quantity) VALUES (?, ?, ?, ?)",
                  (date, title, unit_price, quantity))
        conn.commit()
        conn.close()
        print("Sale added successfully.")
    except ValueError:
        print("Invalid input. Please enter correct data types.")


def view_sales():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM sales")
    records = c.fetchall()
    print("\nID  Date        Title               Unit Price  Quantity  Subtotal")
    print("---------------------------------------------------------------")
    for rec in records:
        subtotal = rec[3] * rec[4]
        print(f"{rec[0]:<3} {rec[1]:<11} {rec[2]:<20} {rec[3]:<10.2f} {rec[4]:<8} {subtotal:<.2f}")
    conn.close()


def update_sale():
    try:
        view_sales()
        sale_id = int(input("Enter the ID of the sale to update: "))
        new_price = float(input("Enter new unit price: "))
        new_qty = int(input("Enter new quantity: "))

        conn = connect_db()
        c = conn.cursor()
        c.execute("UPDATE sales SET unit_price = ?, quantity = ? WHERE id = ?",
                  (new_price, new_qty, sale_id))
        conn.commit()
        conn.close()
        print("Sale updated successfully.")
    except ValueError:
        print("Invalid input. Please enter correct data types.")


def delete_sale():
    try:
        view_sales()
        sale_id = int(input("Enter the ID of the sale to delete: "))
        conn = connect_db()
        c = conn.cursor()
        c.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
        conn.commit()
        conn.close()
        print("Sale deleted successfully.")
    except ValueError:
        print("Invalid ID.")


def print_report():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT book_title, SUM(quantity), SUM(unit_price * quantity) FROM sales GROUP BY book_title")
    records = c.fetchall()
    print("\nTitle               Total Quantity  Total Revenue")
    print("------------------------------------------------")
    for rec in records:
        print(f"{rec[0]:<20} {rec[1]:<14} {rec[2]:.2f}")
    conn.close()


def main():
    init_db()
    while True:
        print("\n**********************************")
        print("1. 新增銷售記錄")
        print("2. 顯示銷售報表")
        print("3. 更新銷售記錄")
        print("4. 刪除銷售記錄")
        print("5. 銷售報表")
        print("0. 離開")
        print("\n**********************************")

        choice = input("Select an option: ")

        if choice == '1':
            add_sale()
        elif choice == '2':
            view_sales()
        elif choice == '3':
            update_sale()
        elif choice == '4':
            delete_sale()
        elif choice == '5':
            print_report()
        elif choice == '0':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()
