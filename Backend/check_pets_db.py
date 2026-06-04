import sqlite3
conn = sqlite3.connect('pet_house.db')
cur = conn.cursor()
print('tables', cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall())
print('pets', cur.execute("SELECT id,name,status FROM pets ORDER BY id DESC LIMIT 10").fetchall())
conn.close()
