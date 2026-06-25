import psycopg2

conn = psycopg2.connect('postgresql://neondb_owner:npg_ReiUD27Fftnw@ep-damp-block-ai81i5p8-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
cur = conn.cursor()

cur.execute("ALTER TABLE pets ADD COLUMN IF NOT EXISTS modalidad VARCHAR DEFAULT 'sede'")
print("OK: ADD COLUMN modalidad")

cur.execute("ALTER TABLE pets ADD COLUMN IF NOT EXISTS telefono_contacto VARCHAR")
print("OK: ADD COLUMN telefono_contacto")

conn.commit()
conn.close()
print("Migración completada.")
