import sqlite3
# from create_bot import db, cursor
db = sqlite3.connect("Fletwix's DataBase.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS MemoryCloud(
userId TEXT,
contentId TEXT,
textOrCaption TEXT,
date TEXT,
dataType TEXT
)""")

cursor.execute("SELECT * FROM MemoryCloud WHERE dataType='photo'")
lst = cursor.fetchall()
print(lst)