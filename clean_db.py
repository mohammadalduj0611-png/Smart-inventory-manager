import sqlite3
import shutil
from pathlib import Path

DB = Path("inventory.db")
BACKUP = Path("inventory_backup_before_clean.db")

if not DB.exists():
    print("ERROR: inventory.db not found.")
    input("Press Enter to close...")
    raise SystemExit

shutil.copy2(DB, BACKUP)

connection = sqlite3.connect(DB)
cursor = connection.cursor()

tables = [
    "sale_items",
    "purchase_items",
    "sales",
    "purchases",
    "expenses",
    "products",
    "categories",
    "customers",
    "suppliers",
]

for table in tables:
    cursor.execute(f'DELETE FROM "{table}"')

connection.commit()
connection.close()

print("====================================")
print("Clean database created successfully!")
print("====================================")
print(f"Backup: {BACKUP}")
print("")

input("Press Enter to close...")