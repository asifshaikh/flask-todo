import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())
curr = conn.cursor()

tasks = [
    ('Learn Flask','Conplete the Flask tutorial', 0),
    ('Build a web app','Create a to-do web application', 0),
    ('Deploy the app','Deploy the app to a cloud service', 0)
]
curr.executemany('INSERT INTO tasks (title, description, completed) VALUES (?,?,?)', tasks)
conn.commit()
conn.close()
print("Database and table created, sample data inserted.")