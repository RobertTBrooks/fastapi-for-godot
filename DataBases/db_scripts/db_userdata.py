import sqlite3

# 1. This creates a file named 'game_data.db'
connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()

# 2. Create a table with two columns: an ID and a Message
cursor.execute("""
        ALTER TABLE userdata ADD COLUMN last_seen INTEGER NOT NULL DEFAULT 0;
""")
cursor.execute("""
        ALTER TABLE userdata ADD COLUMN session_id TEXT;
""")
connection.commit()
connection.close()

print("Database created successfully!")