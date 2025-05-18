# from client import get_json_data
from client import db_client

# Humitat
from routers.humitat import humitats_schema

# Planta
from routers.planta import plantes_schema

# Sensors
from routers.sensors import sensors_schema

# Usuaris
from routers.usuaris import usuaris_schema

# -------------------------------------------------------------- USUARI --------------------------------------------------------------  
# GET: Llegeix tots els usuaris
def get_usuaris():
    try:
        conn = db_client()
        cursor = conn.cursor()

        query = "SELECT * FROM usuaris"
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return usuaris_schema(result)

    except Exception as e:
        return {"status": -1, "message": f"Error al llegir usuaris: {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# GET: Llegeix un usuari per id  
def get_usuari_by_id(id_usuari: int):
    try:
        conn = db_client()
        cursor = conn.cursor()
        
        query = "SELECT * FROM usuaris WHERE id = %s"
        cursor.execute(query, (id_usuari,))
        
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()
        
        if result:
            return dict(zip(columns, result))
        else:
            return None
            
    except Exception as e:
        return {"status": -1, "message": f"Error al buscar usuario: {str(e)}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# POST: Crea un usuari nou
from security import hash_password  # Importo la funció de hashing (encriptar les contrasenyes)
def create_usuari(usuari_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        # Hashea les contrasenyes aans d'emmagatzemar-les
        hashed_password = hash_password(usuari_data.contrasenya)

        query = """
        INSERT INTO usuaris (nom, cognom, email, contrasenya, sensor_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, nom, email
        """

        values = (
            usuari_data.nom,
            usuari_data.cognom,
            usuari_data.email,
            hashed_password, 
            usuari_data.sensor_id if hasattr(usuari_data, 'sensor_id') else None
        )

        cur.execute(query, values)
        conn.commit()

        result = cur.fetchone()
        if result:
            return {
                "id": result[0],
                "nom": result[1],
                "email": result[2],
                "status": 1,
                "message": "Usuari creat correctament"
            }
        return {"status": -1, "message": "No s'ha pogut crear l'usuari"}

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error en create_usuari: {e}")
        return {"status": -1, "message": f"Error: {e}"}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
   
# DELETE: Eliminem un usuari per la seva id
def delete_usuari_by_id(id_usuari: int):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "DELETE FROM usuaris WHERE id = %s"
        cur.execute(query, (id_usuari,))
        conn.commit()

        if cur.rowcount == 0:
            return {"status": -1, "message": "Usuari no trobat"}

        return {"status": 1, "message": f"Usuari amb ID {id_usuari} eliminat correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error: {str(e)}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
# UPDATE: Actualitzo l'usuari per id
def update_usuari(id_usuari: int, dades_update: dict):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE usuaris
            SET nom = %s, cognom = %s, email = %s, contrasenya = %s, sensor_id = %s
            WHERE id = %s
        """
        values = (
            dades_update.get("nom"),
            dades_update.get("cognom"),
            dades_update.get("email"),
            dades_update.get("contrasenya"),
            dades_update.get("sensor_id"),
            id_usuari
        )
        cur.execute(query, values)
        updated_recs = cur.rowcount
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return updated_recs

# ---------------------- USUARI i PLANTA ----------------------  
# GET: per llegir les plantes que te cada usuari
def read_plantes_by_usuari_id(usuari_id: int):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT id, nom, ubicacio, sensor_id, usuari_id, imagen_url FROM planta WHERE usuari_id = %s"
        cur.execute(query, (usuari_id,))
        rows = cur.fetchall()

        if not rows:
            return []

        columns = ["id", "nom", "ubicacio", "sensor_id", "usuari_id", "imagen_url"]
        plantes = [dict(zip(columns, row)) for row in rows]

        return plantes

    except Exception as e:
        print(f"Error en read_plantes_by_usuari_id: {e}")
        return {"status": -1, "message": f"Error a la BBDD: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
# ---------------------- /USUARI i PLANTA ----------------------

# -------------------------- FUNCIÓ LOGIN --------------------------
from security import verify_password
from client import db_client
import psycopg2
from psycopg2.extras import RealDictCursor

# Funció per el LOGIN
from psycopg2.extras import RealDictCursor

def check_credentials(email: str, contrasenya: str):
    conn = None
    cursor = None
    try:
        conn = db_client()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM usuaris WHERE email = %s", (email,))
        usuari = cursor.fetchone()

        if usuari is None:
            return {"status": -1, "message": "Usuari no trobat"}

        from security import verify_password
        if not verify_password(contrasenya, usuari["contrasenya"]):
            return {"status": -1, "message": "Contrasenya incorrecta"}

        usuari.pop("contrasenya", None)
        return {"status": 1, "usuari": usuari}

    except Exception as e:
        return {"status": -1, "message": f"Error: {str(e)}"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------- /FUNCIÓ LOGIN --------------------------
# -------------------------------------------------------------- /USUARI --------------------------------------------------------------  


# -------------------------------------------------------------- PLANTA --------------------------------------------------------------  
# GET: Obtenim totes les plantes registrades
def get_plantes():
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT id, nom, ubicacio, sensor_id, usuari_id, imagen_url FROM planta"
        cur.execute(query)
        rows = cur.fetchall()

        columns = ["id", "nom", "ubicacio", "sensor_id", "usuari_id", "imagen_url"]
        plantes = [dict(zip(columns, row)) for row in rows]

        return plantes

    except Exception as e:
        return {"status": -1, "message": f"Error en llegir plantes: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# GET: Llegeix una planta per ID
def read_planta_by_id(planta_id: int):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "SELECT id, nom, ubicacio, sensor_id, usuari_id, imagen_url FROM planta WHERE id = %s"
        cur.execute(query, (planta_id,))
        row = cur.fetchone()

        if row is None:
            return None

        columns = ["id", "nom", "ubicacio", "sensor_id", "usuari_id", "imagen_url"]
        return dict(zip(columns, row))

    except Exception as e:
        return {"status": -1, "message": f"Error en llegir la planta: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# POST: Crearem una planta
def create_planta(planta_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
            INSERT INTO planta (nom, ubicacio, sensor_id, usuari_id, imagen_url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """

        values = (
            planta_data.nom,
            planta_data.ubicacio,
            planta_data.sensor_id,
            planta_data.usuari_id,
            planta_data.imagen_url
        )

        cur.execute(query, values)
        conn.commit()
        new_id = cur.fetchone()[0]

        return {"status": 1, "message": "Planta creada correctament", "id": new_id}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en crear la planta: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# DELETE: Elimina una planta per id            
def delete_planta(planta_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "DELETE FROM planta WHERE id = %s"
        cur.execute(query, (planta_id,))
        conn.commit()

        if cur.rowcount == 0:
            return {"status": -1, "message": "Planta no trobada"}

        return {"status": 1, "message": f"Planta amb ID {planta_id} eliminada correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en eliminar planta: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#UPDATE: Actualitza una planta per id
def update_planta(planta_id: int, planta_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE planta
            SET nom = %s, ubicacio = %s, sensor_id = %s, usuari_id = %s, imagen_url = %s
            WHERE id = %s
        """
        values = (
            planta_data.nom,
            planta_data.ubicacio,
            planta_data.sensor_id,
            planta_data.usuari_id,
            planta_data.imagen_url,
            planta_id
        )
        cur.execute(query, values)
        updated = cur.rowcount
        conn.commit()

        if updated == 0:
            return {"status": -1, "message": "No s'ha trobat cap planta per modificar"}

        return {"status": 1, "message": "Planta actualitzada correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en actualitzar planta: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
# -------------------------------------------------------------- /PLANTA --------------------------------------------------------------  


# -------------------------------------------------------------- SENSORS --------------------------------------------------------------  
# GET: Llegeix tots els sensors
def get_all_sensors():
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT sensor_id, estat, usuari_id FROM sensors"
        cur.execute(query)
        rows = cur.fetchall()

        columns = ["sensor_id", "estat", "usuari_id"]
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        return {"status": -1, "message": f"Error en obtenir sensors: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# GET: Llegeix sol els sensors per id
def get_sensor_by_id(sensor_id: int):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT sensor_id, estat, usuari_id FROM sensors WHERE sensor_id = %s"
        cur.execute(query, (sensor_id,))
        row = cur.fetchone()

        if row is None:
            return None

        columns = ["sensor_id", "estat", "usuari_id"]
        return dict(zip(columns, row))

    except Exception as e:
        return {"status": -1, "message": f"Error en obtenir el sensor: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
# POST: Crearem un nou Sensor (producte)
def create_sensor(sensor_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
            INSERT INTO sensors (estat, usuari_id)
            VALUES (%s, %s)
            RETURNING sensor_id
        """
        values = (sensor_data.estat, sensor_data.usuari_id)
        cur.execute(query, values)
        conn.commit()

        new_id = cur.fetchone()[0]
        return {"status": 1, "message": "Sensor creat correctament", "sensor_id": new_id}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en crear el sensor: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# DELETE: Elimina un sensor per id
def delete_sensor(sensor_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "DELETE FROM sensors WHERE sensor_id = %s"
        cur.execute(query, (sensor_id,))
        conn.commit()

        if cur.rowcount == 0:
            return {"status": -1, "message": "Sensor no trobat"}

        return {"status": 1, "message": f"Sensor amb ID {sensor_id} eliminat correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en eliminar sensor: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# UPDATE: Actualitza un sensor per id
def update_sensor(sensor_id: int, sensor_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE sensors
            SET estat = %s, usuari_id = %s
            WHERE sensor_id = %s
        """
        values = (sensor_data.estat, sensor_data.usuari_id, sensor_id)
        cur.execute(query, values)
        updated = cur.rowcount
        conn.commit()

        if updated == 0:
            return {"status": -1, "message": "Sensor no trobat per actualitzar"}

        return {"status": 1, "message": "Sensor actualitzat correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en actualitzar sensor: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
# -------------------------------------------------------------- /SENSORS --------------------------------------------------------------  


# -------------------------------------------------------------- HUMITAT SOL --------------------------------------------------------------  
# GET: Llegeix totes les humitats
def get_all_humitats():
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT id, sensor_id, valor, timestamp FROM humitat_sol"
        cur.execute(query)
        rows = cur.fetchall()

        columns = ["id", "sensor_id", "valor", "timestamp"]
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        return {"status": -1, "message": f"Error en obtenir humitats: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# GET: Llegeix les humitats per id
def get_humitat_by_id(humitat_id: int):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT id, sensor_id, valor, timestamp FROM humitat_sol WHERE id = %s"
        cur.execute(query, (humitat_id,))
        row = cur.fetchone()

        if row is None:
            return None

        columns = ["id", "sensor_id", "valor", "timestamp"]
        return dict(zip(columns, row))

    except Exception as e:
        return {"status": -1, "message": f"Error en obtenir la humitat: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
# POST: Creare una nova humitat - mirar a classe
def create_humitat(humitat_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()

        query = """
            INSERT INTO humitat_sol (sensor_id, valor)
            VALUES (%s, %s)
            RETURNING id
        """
        values = (humitat_data.sensor_id, humitat_data.valor)
        cur.execute(query, values)
        conn.commit()

        new_id = cur.fetchone()[0]
        return {"status": 1, "message": "Humitat registrada", "id": new_id}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en registrar humitat: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# DELETE: Elimina una humitat per id:
def delete_humitat(humitat_id: int):
    try:
        conn = db_client()
        cur = conn.cursor()

        query = "DELETE FROM humitat_sol WHERE id = %s"
        cur.execute(query, (humitat_id,))
        conn.commit()

        if cur.rowcount == 0:
            return {"status": -1, "message": "Humitat no trobada"}

        return {"status": 1, "message": f"Humitat amb ID {humitat_id} eliminada correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en eliminar humitat: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# UPDATE: Actualitza l'humitat sol passant una id:
def update_humitat(humitat_id: int, humitat_data):
    conn = None
    cur = None
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """
            UPDATE humitat_sol
            SET sensor_id = %s, valor = %s
            WHERE id = %s
        """
        values = (humitat_data.sensor_id, humitat_data.valor, humitat_id)
        cur.execute(query, values)
        updated = cur.rowcount
        conn.commit()

        if updated == 0:
            return {"status": -1, "message": "Humitat no trobada per modificar"}

        return {"status": 1, "message": "Humitat actualitzada correctament"}

    except Exception as e:
        if conn:
            conn.rollback()
        return {"status": -1, "message": f"Error en actualitzar humitat: {e}"}

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
# -------------------------------------------------------------- /HUMITAT SOL --------------------------------------------------------------  