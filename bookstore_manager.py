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
            member_name TEXT NOT NULL,
            book_title TEXT NOT NULL,
            unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_sale():
    try:
        date = input("請輸入銷售日期 (YYYY-MM-DD): ")
        datetime.datetime.strptime(date, '%Y-%m-%d')
        member = input("請輸入會員名稱：")
        title = input("請輸入書籍名稱：")
        unit_price = float(input("請輸入單價："))
        quantity = int(input("請輸入購買數量："))

        conn = connect_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO sales (date, member_name, book_title, unit_price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, member, title, unit_price, quantity))
        conn.commit()
        conn.close()
        print("銷售記錄新增成功.")
    except ValueError:
        print("輸入無效，請確認日期格式、價格與數量為正確數值。")


def view_sales():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM sales")
    records = c.fetchall()
    print("\nID  Date        Member   Title               Unit Price  Quantity  Subtotal")
    print("----------------------------------------------------------------------------")
    for rec in records:
        subtotal = rec[4] * rec[5]
        print(f"{rec[0]:<3} {rec[1]:<11} {rec[2]:<8} {rec[3]:<20} {rec[4]:<10.2f} {rec[5]:<8} {subtotal:<.2f}")
    conn.close()


def update_sale():
    try:
        view_sales()
        sale_id = int(input("輸入要更新的銷售 ID："))
        new_price = float(input("輸入新的單價："))
        new_qty = int(input("輸入新數量："))

        conn = connect_db()
        c = conn.cursor()
        c.execute("UPDATE sales SET unit_price = ?, quantity = ? WHERE id = ?",
                  (new_price, new_qty, sale_id))
        conn.commit()
        conn.close()
        print("✅ 銷售記錄更新成功.")
    except ValueError:
        print("❌ 輸入無效，請輸入正確的數字類型。")


def delete_sale():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, member_name, date FROM sales")
        records = c.fetchall()

        if not records:
            print("⚠️ 沒有任何銷售記錄可供刪除。")
            return

        print("\n======== 銷售記錄列表 ========")
        for idx, (sale_id, member, date) in enumerate(records, 1):
            print(f"{idx}. 銷售編號: {sale_id} - 會員: {member} - 日期: {date}")
        print("================================")

        user_input = input("請選擇要刪除的銷售編號 (輸入數字或按 Enter 取消): ").strip()
        if user_input == "":
            print("已取消刪除操作。")
            return
        if not user_input.isdigit():
            print("=> 錯誤：請輸入有效的數字")
            return

        sale_id = int(user_input)
        c.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
        conn.commit()
        conn.close()
        print(f"銷售編號 {sale_id} 已刪除。")
    except ValueError:
        print("錯誤：請輸入有效的數字。")


def main():
    init_db()
    while True:
        print("\n***************選單***************")
        print("1. 新增銷售記錄")
        print("2. 顯示銷售記錄")
        print("3. 更新銷售記錄")
        print("4. 刪除銷售記錄")
        print("5. 離開")
        print("**********************************")

        choice = input("請選擇操作項目(Enter 離開)：: ").strip()

        if choice == '1':
            add_sale()
        elif choice == '2':
            view_sales()
        elif choice == '3':
            update_sale()
        elif choice == '4':
            delete_sale()
        elif choice == '5' or choice == '':
            print("👋 離開系統，再見！")
            break
        else:
            print("=> 錯誤：請輸入有效的選項。")


if __name__ == '__main__':
    main()
