import pandas as pd
import psycopg2

# Load the CSV
df = pd.read_csv(r"C:\Users\Yuvaraj\Pictures\employees_leave_1.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="workwise_ai",
    user="postgres",
    password="postgres",
    host="localhost",  # or the appropriate host
    port="5432"
)
cursor = conn.cursor()

# Insert row by row
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO hrms_employees (
            id, resource_id, private_country_id, country_id, name, job_title,
            work_phone, mobile_phone, work_email, private_street, private_street2,
            private_city, private_zip, private_phone, private_email, lang, gender,
            marital, place_of_birth, employee_type, birthday, create_date, write_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
    
conn.commit()
cursor.close()
conn.close()
