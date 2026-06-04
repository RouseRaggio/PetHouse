import psycopg2
conn = psycopg2.connect('postgresql://neondb_owner:npg_ReiUD27Fftnw@ep-damp-block-ai81i5p8-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
cur = conn.cursor()
cur.execute("ALTER TABLE adoptions ADD COLUMN IF NOT EXISTS quiere_tracker BOOLEAN DEFAULT FALSE")
print('OK: ALTER TABLE adoptions ADD COLUMN IF NOT EXISTS quiere_tracker BOOLEAN DEFAULT FALSE')
conn.commit()
conn.close()
