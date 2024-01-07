import psycopg2
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE clients;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL,
                phones INTEGER
            );
            """)
        conn.commit()
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(first_name, last_name, email, phones)
            VALUES (%s, %s, %s, %s);      
        """, (first_name, last_name, email, phones))
        conn.commit()
def add_phone(conn, client_id, phones):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET phones=%s WHERE id=%s;
        """,(phones, client_id))
        conn.commit()
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET first_name=%s, last_name=%s, email=%s, phones=%s WHERE id=%s;
        """, (first_name, last_name, email, phones, client_id))
        conn.commit()
def delete_phone(conn, client_id, phones):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET phones=NULL WHERE id=%s AND phones=%s;
        """, (client_id, phones))
        conn.commit()
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients WHERE id=%s;
        """, (client_id,))
        conn.commit()
def find_client(conn, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM clients WHERE first_name=%s OR last_name=%s OR email=%s OR phones=%s;
        """, (first_name, last_name, email, phones))
        return cur.fetchone()[0]


with psycopg2.connect(database='', user='', password='') as conn:
    create_db(conn)
    add_client(conn, 'Ivan', 'Coi', '1234@mail.ru', 12345)
    add_client(conn, 'sd', 'wd', 'sasd')
    add_phone(conn, 2, 123)
    change_client(conn, 2, 'sd', 'ia', 'ji', 123)
    delete_phone(conn, 2, 123)
    delete_client(conn, 1)
    print(find_client(conn, first_name='sd'))


conn.close()
