from client import db_client
def connectar():
    return db_client()

# ----------------------------------- SELECT TAULA PLANTA -----------------------------------
def read_plantes():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM planta")
        rows = cur.fetchall()

        columns = ["id", "nom", "sensor_id"]
        plantes = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

    return plantes

# Llegeixo sol la planta buscada per id
def read_planta_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM planta WHERE id = %s"
        value = (id,)
        cur.execute(query, value)

        planta = cur.fetchone()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}

    finally:
        conn.close()

    return planta
# ----------------------------------- /SELECT TAULA PLANTA -----------------------------------


# ----------------------------------- SELECT TAULA USUARIS -----------------------------------
# Mostra tots els usuaris
def get_usuaris():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT id_usuari, nom, cognom, email, contrasenya, sensor_id FROM usuaris")
        rows = cur.fetchall()

        # Claus per JSON
        columns = ["id_usuari", "nom", "cognom", "email", "contrasenya", "sensor_id"]
        usuaris = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

    return usuaris

# Mostra els usuaris per id
def read_usuari_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM usuaris WHERE id_usuari = %s"
        value = (id,)
        cur.execute(query, value)

        usuari = cur.fetchone()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}

    finally:
        conn.close()

    return usuari
# ----------------------------------- /SELECT TAULA USUARIS -----------------------------------


# ----------------------------------- SELECT TAULA SENSORS -----------------------------------
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
# ----------------------------------- /SELECT TAULA SENSORS -----------------------------------


# -----------------------------------  SELECT TAULA HUMITAT_SOL -----------------------------------
# Mostro les humitats de cada sensor
def get_humitat():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM humitat_sol")
        rows = cur.fetchall()

        columns = ["id", "sensor_id", "valor", "timestamp"]
        humitats = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

    return humitats


def get_valors_humitat():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT valor FROM humitat_sol") # Sol agafo el valor
        rows = cur.fetchall()

        valors = [row[0] for row in rows]  # Només extreiem el valor (float)

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

    return valors

# Mostro les humitats de cada sensor per idl
def read_humitatSol_id(humitatSol_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM humitat_sol WHERE id=%s"

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

# -----------------------------------  /SELECT TAULA HUMITAT_SOL -----------------------------------

# ------------------------------------- CREATE -----------------------------------
