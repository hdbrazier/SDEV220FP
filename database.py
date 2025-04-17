import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS appointments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  time TEXT NOT NULL,
  client TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Database and table created.")
