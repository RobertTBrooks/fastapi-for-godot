import sqlite3

# 1. This creates a file named 'game_data.db'
connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()

# 2. Create a table with two columns: an ID and a Message
cursor.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
""")

connection.commit()
connection.close()

print("Database created successfully!")