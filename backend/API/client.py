import psycopg2

def db_client():
    try:
        return psycopg2.connect(
            host="127.0.0.1",     # localhost
            port="5433",
            user="admin",
            password="ITIC_BCN",
            database="ecosense_db"
        )
    except Exception as e:
        print(f"Error de conexión: {e}")
        raise