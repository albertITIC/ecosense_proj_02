from client import db_client
def connectar():
    return db_client()

# ----------------------------------- SELECT TAULA PLANTA -----------------------------------
def read_plantes():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT id, nom, sensor_id, usuari_id FROM planta")
        rows = cur.fetchall()

        columns = ["id", "nom", "sensor_id", "usuari_id"]
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

# Mostro les plantes que te l'usuari
def read_plantes_by_usuari_id(usuari_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT id, nom, sensor_id, usuari_id FROM planta WHERE usuari_id = %s"
        cur.execute(query, (usuari_id,))
        rows = cur.fetchall()

        if not rows:
            return []

        columns = ["id", "nom", "sensor_id", "usuari_id"]
        plantes = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Error en read_plantes_by_usuari_id: {e}")
        return {"status": -1, "message": f"Error a la BBDD: {e}"}

    finally:
        conn.close()

    return plantes


# ----------------------------------- /SELECT TAULA PLANTA -----------------------------------


# ----------------------------------- SELECT TAULA USUARIS -----------------------------------
# Mostra tots els usuaris
def get_usuaris():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT id, nom, cognom, email, contrasenya, sensor_id FROM usuaris")
        rows = cur.fetchall()

        # Claus per JSON
        columns = ["id", "nom", "cognom", "email", "contrasenya", "sensor_id"]
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
        query = "SELECT id, nom, cognom, email, contrasenya, sensor_id FROM usuaris WHERE id_usuari = %s"
        value = (id,)
        cur.execute(query, value)

        row = cur.fetchone()
        
        if row is None:
            return None

        # Claus per JSON (mateixes que a get_usuaris)
        columns = ["id", "nom", "cognom", "email", "contrasenya", "sensor_id"]
        usuari = dict(zip(columns, row))

    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}

    finally:
        conn.close()

    return usuari
# ----------------------------------- /SELECT TAULA USUARIS -----------------------------------

# ----------------------------------- CREAR USUARIS -----------------------------------
# Per la creació de la contrasenya encriptada
# from utils.security import hash_contrasenya
# Crear un usuari nou a la base de dades
# def crear_usuari(nom, cognom, email, contrasenya):
#     try:
#         conn = db_client()
#         cursor = conn.cursor()

#         # Encriptar la contrasenya abans de guardar-la
#         contrasenya_hash = hash_contrasenya(contrasenya)

#         # Inserir l'usuari nou
#         query = "INSERT INTO usuaris (nom, cognom, email, contrasenya) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (nom, cognom, email, contrasenya_hash))

#         conn.commit()

#         return {
#             "msg": "S'ha creat l'usuari correctament",
#             "nom": nom,
#             "email": email
#         }

#     except Exception as e:
#         return {"status": -1, "message": str(e)}

#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
            
# from .connexio import db_client  # o ajusta según tu estructura

def create_usuari(usuari_data):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
        INSERT INTO usuaris (nom, cognom, email, contrasenya, sensor_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_usuari
        """

        values = (
            usuari_data.nom,
            usuari_data.cognom,
            usuari_data.email,
            usuari_data.contrasenya,
            usuari_data.sensor_id
        )

        cur.execute(query, values)
        conn.commit()

        id_nou = cur.fetchone()[0]

    except Exception as e:
        print(f"Error en create_usuari: {e}")
        return {"status": -1, "message": f"Error a la BBDD: {e}"}

    finally:
        conn.close()

    return id_nou
# ----------------------------------- /CREAR USUARIS -----------------------------------

# ----------------------------------- DELETE USUARIS -----------------------------------
def delete_usuari(id_usuari: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        # Verificar si existe
        cur.execute("SELECT * FROM usuaris WHERE id = %s", (id,))
        if cur.fetchone() is None:
            return {"status": 0, "message": f"No existeix cap usuari amb ID {id}"}

        # Eliminar
        cur.execute("DELETE FROM usuaris WHERE id_usuari = %s", (id,))
        conn.commit()

    except Exception as e:
        print(f"Error en delete_usuari: {e}")
        return {"status": -1, "message": f"Error a la BBDD: {e}"}

    finally:
        conn.close()

    return {"status": 1, "message": f"Usuari amb ID {id_usuari} eliminat correctament"}

# ----------------------------------- /DELETE USUARIS -----------------------------------





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
