from client import db_client
def connectar():
    return db_client()


def read_plantes():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM planta")
        rows = cur.fetchall()

        # Definim els noms de les columnes de la meva taula (això ho faig perquè la sortida per pantalla sigui més clara)
        columns = ["id", "nom", "sensor_id"]
        plantes = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

    return plantes

# Retorno una planta buscada per id
def read_planta_id(planta_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT * FROM planta WHERE id = %s"
        cur.execute(query, (planta_id,))
        result = cur.fetchone()

        if result is None:
            return None

        columns = ["id", "nom", "sensor_id"]
        planta = dict(zip(columns, result))

        return planta

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

# Mostra tots els usuaris
def read_usuaris():
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT * FROM usuaris"
        cur.execute(query)
        rows = cur.fetchall()

        columns = ["usuari_id", "nom", "cognom", "email", "email", "contrasenya", "sensor_id"]
        usuaris = [dict(zip(columns, row)) for row in rows]

        return usuaris

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

# Mostra els usuaris per id
def read_usuari_id(usuari_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT * FROM usuaris WHERE id_usuari = %s"
        cur.execute(query, (usuari_id,))
        result = cur.fetchone()

        if result is None:
            return None

        columns = ["id_usuari", "nom", "cognom", "email", "email", "contrasenya", "sensor_id"]
        usuari = dict(zip(columns, result))

        return usuari

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()


# Mostro els sensors (productes?)
def read_sensors():
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT * FROM sensors"
        cur.execute(query)
        rows = cur.fetchall()

        columns = ["sensor_id", "ubicacio", "planta", "estat"]
        sensors = [dict(zip(columns, row)) for row in rows]

        return sensors

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

# Mostro els sensors per id
def  read_sensors_id(sensor_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT * FROM sensors WHERE sensor_id = %s"
        cur.execute(query, (sensor_id,))
        result = cur.fetchone()

        if result is None:
            return None

        columns = ["sensor_id", "ubicacio", "planta", "estat"]
        sensor = dict(zip(columns, result))

        return sensor

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

# Mostro les humitats de cada sensor
def read_humitatSol():
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM humitat_sol"
        cur.execute(query)

        rows = cur.fetchall()

        if not rows:  # Més correcte que 'is None' per a fetchall()
            return None

        columns = ["id", "sensor_id", "valor", "timestamp"]
        humitats = [dict(zip(columns, row)) for row in rows]  # Llista de diccionaris

        return humitats

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

# Mostro les humitats de cada sensor per id
def read_humitatSol_id(humitatSol_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM humitat_sol WHERE id = %s"

        cur.execute(query, (humitatSol_id,))
        result = cur.fetchone()

        if result is None:
            return None

        columns = ["id", "sensor_id", "valor", "timestamp"]
        humitat_sol = dict(zip(columns, result))

        return humitat_sol

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()
