from db_connection import get_connection

# SELECT
def get_new_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registration_data WHERE status='NEW'")
    data = cursor.fetchall()
    conn.close()
    return data


# INSERT
def insert_user(data):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO registration_data 
    (first_name,last_name,address,city,state,zip_code,phone,ssn,username,password)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, data)
    conn.commit()
    conn.close()

