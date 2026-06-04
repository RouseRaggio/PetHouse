import psycopg2
conn = psycopg2.connect('postgresql://neondb_owner:npg_ReiUD27Fftnw@ep-damp-block-ai81i5p8-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
cur = conn.cursor()
cur.execute("SELECT table_name, column_name FROM information_schema.columns WHERE table_name IN ('users','pets') AND column_name IN ('gps_status','gps_imei') ORDER BY table_name, column_name")
print(cur.fetchall())
conn.close()
