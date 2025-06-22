import csv
import sqlite3
import os

FOLDER = 'data_csv'  # Folder with all your CSV files

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS items')
cursor.execute('''
CREATE TABLE items (
    id TEXT PRIMARY KEY,
    name TEXT,
    quantity INTEGER
)
''')

for filename in os.listdir(FOLDER):
    if filename.endswith(".csv"):
        path = os.path.join(FOLDER, filename)
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    cursor.execute("INSERT INTO items (id, Name, quantity) VALUES (?, ?, ?)",
                                   (row['id'], row['Name'], int(row['quantity'])))
                except sqlite3.IntegrityError:
                    print(f"Duplicate item ID skipped: {row['id']}")

conn.commit()
conn.close()
print("✅ Merged all CSV files into inventory.db")
