import psycopg2
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE clients_phones;
            DROP TABLE clients;
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients_phones(
                id SERIAL PRIMARY KEY,
                clients_id INTEGER REFERENCES clients(id),
                phones INTEGER
            );
        """)
        conn.commit()
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id;      
        """, (first_name, last_name, email))
        clients_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO clients_phones(phones, clients_id)
            VALUES (%s, %s);
        """, (phones, clients_id))
        conn.commit()
def add_phone(conn, client_id, phones):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients_phones SET phones=%s WHERE clients_id=%s;
        """,(phones, client_id))
        conn.commit()
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET first_name=%s WHERE id=%s AND first_name=%s IS NOT NULL;
        """, (first_name, client_id, first_name))
        cur.execute("""
            UPDATE clients SET last_name=%s WHERE id=%s AND last_name=%s IS NOT NULL;   
        """, (last_name, client_id, last_name))
        cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s AND email=%s IS NOT NULL;   
        """, (email, client_id, email))
        cur.execute("""
            UPDATE clients_phones SET phones=%s WHERE clients_id=%s AND phones=%s IS NOT NULL;   
        """, (phones, client_id, phones))
        conn.commit()
def delete_phone(conn, client_id, phones):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients_phones SET phones=NULL WHERE clients_id=%s AND phones=%s;
        """, (client_id, phones))
        conn.commit()
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM clients_phones WHERE clients_id=%s;
                """, (client_id,))
        cur.execute("""
            DELETE FROM clients WHERE id=%s;
        """, (client_id,))
        conn.commit()
def find_client(conn, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, cp.phones FROM clients c
            JOIN clients_phones cp ON c.id = cp.clients_id
            WHERE first_name=%s AND first_name=%s IS NOT NULL OR last_name=%s AND last_name=%s IS NOT NULL OR email=%s AND email=%s IS NOT NULL OR phones=%s AND phones=%s IS NOT NULL;
        """, (first_name, first_name, last_name, last_name, email, email, phones, phones))
        return cur.fetchone()
if __name__ == "__main__":
    with psycopg2.connect(database='', user='', password='') as conn:
        create_db(conn)
        add_client(conn, 'Ivan', 'Coi', '1234@mail.ru', 12345)
        add_client(conn, 'sd', 'wd', 'sasd')
        add_phone(conn, 2, 123)
        change_client(conn, 2, 'ji')
        delete_phone(conn, 1, 12345)
        delete_client(conn, 1)
        print(find_client(conn, phones=123))

    conn.close()