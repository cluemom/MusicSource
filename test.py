import os
os.add_dll_directory(r"C:\Program Files\PostgreSQL\17\bin")  # Adjust to your PostgreSQL path

import psycopg2
conn = psycopg2.connect(
    dbname="musicsource_db",
    user="sterfry",
    password="your_password",
    host="localhost",
    port="5432"
)
print("Connection successful!")
conn.close()
