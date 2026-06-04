import psycopg2
conn = psycopg2.connect('postgresql://neondb_owner:npg_ReiUD27Fftnw@ep-damp-block-ai81i5p8-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
cur = conn.cursor()
statements = [
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS gps_status VARCHAR DEFAULT 'none'",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS gps_imei VARCHAR",
    "ALTER TABLE pets ADD COLUMN IF NOT EXISTS gps_status VARCHAR DEFAULT 'none'",
    "ALTER TABLE pets ADD COLUMN IF NOT EXISTS gps_imei VARCHAR",
]
for sql in statements:
    cur.execute(sql)
    print('OK:', sql)
conn.commit()
conn.close()
