import sqlite3

connection = sqlite3.connect("inventory.db")
cursor = connection.cursor()

tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("TABLES:")
for table in tables:
    print("-", table[0])

connection.close()

input("\nPress Enter to close...")