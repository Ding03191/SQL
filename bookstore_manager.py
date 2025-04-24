import sqlite3

conn = sqlite3.connect('bookstore.db')  # 連線資料庫
cursor = conn.cursor()  # 建立 cursor 物件

# 啟用外鍵約束
conn.execute("PRAGMA foreign_keys = ON;")

# 查詢
cursor.execute("SELECT * FROM customer")
data = cursor.fetchall()  # 取得所有資料
print(type(data))  # <class 'list'>

for rec in data:
    print(type(rec))  # <class 'tuple'>
    print(f"ID：{rec[0]}, Name：{rec[1]}, Tel：{rec[2]}, Addr：{rec[3]}")

# 新增
cursor.execute(
    "INSERT INTO customer (cid, cname, ctel, cadd) VALUES (?, ?, ?, ?)",
    ('c004', 'Cathy', '0937-543889', 'Tainan City daye road'),
)

conn.commit()  # 寫入資料庫
cursor.close()  # 關閉 cursor 物件
conn.close()  # 關閉資料庫連線
