import sqlite3

# 1. This creates a file named 'game_data.db'
connection = sqlite3.connect("chat_data.db")
cursor = connection.cursor()

# 2. Create a table with two columns: an ID and a Message
cursor.execute("""
    CREATE TABLE IF NOT EXISTS storage (
        id INTEGER PRIMARY KEY,
        message TEXT
    )
""")

# 3. Put an initial "row" of data in so it's not empty
cursor.execute("INSERT INTO storage (id, message) VALUES (1, 'Hello from SQLite')")

connection.commit()
connection.close()

print("Database created successfully!")