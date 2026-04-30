import sqlite3
conn = sqlite3.connect('pet_house.db')
cursor = conn.cursor()

statuses = [
    (1, 'PENDING', 0, 1),
    (2, 'APPROVED', 1, 2),
    (3, 'REJECTED', 1, 3)
]

for s in statuses:
    cursor.execute('''
        INSERT OR IGNORE INTO adoption_status (id, name, is_final, "order")
        VALUES (?, ?, ?, ?)
    ''', s)

conn.commit()
conn.close()
print('Adoption statuses seeded.')
