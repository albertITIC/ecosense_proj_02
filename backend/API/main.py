from typing import List
from fastapi import FastAPI, HTTPException
import db_plantes
from db_plantes import db_client
from pydantic import BaseModel
from schemas import humitat_sol, planta, sensors, usuaris


# Importo les querys
from db_plantes import read_plantes, read_planta_id
from db_plantes import get_usuaris, read_usuari_id
from db_plantes import read_sensors, read_sensors_id
from db_plantes import get_humitat, read_humitatSol_id

app = FastAPI()

# --------------------------------- MODELS ---------------------------------
# Creació de les taules BaseModel
class humitat_sol(BaseModel):
    id: int
    sensor_id: int
    valor: float
    timestamp : int

class planta(BaseModel):
    id: int
    nom: str
    sensor_id: int

class sensors(BaseModel):
    sensor_id: int
    ubicacio: str
    planta: str
    estat: str

class usuaris(BaseModel):
    id_usuari: int
    nom: str
    cognom: str
    email: str
    contrasenya: str
    sensor_id: int
# --------------------------------- /MODELS ---------------------------------


# --------------------------------- GETS INICIALS ---------------------------------
# Endpoint inicial
@app.get("/")
def index():
    return {"Missatge": "Benvilgut a l'API Ecosense"}

# Comprova que hi hagi connexió
@app.get("/prova-connexio")
def prova_connexio():
    try:
        conn = db_client()
        conn.close()
        return {"connexio": "correcta"}
    except Exception as e:
        return {"error": str(e)}
# --------------------------------- /GETS INICIALS ---------------------------------

# --------------------------------- PLANTES ---------------------------------
# ---------------- SELECT PLANTES ----------------
# Llegim totes les plantes
@app.get("/plantes/list", response_model=List[dict])
def read_all_plantes():
    try:
        plantes = db_plantes.read_plantes()

        if isinstance(plantes, dict) and plantes.get("status") == -1:
            raise HTTPException(
                status_code=500,
                detail=plantes["message"]
            )

        columns = ["id", "nom", "sensor_id"]
        plantes_list = [dict(zip(columns, planta)) for planta in plantes]

        return [{"plantes": plantes_list}]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


# Llegim UNA planta en concret, passo l'id
@app.get("/plantes/{id}", response_model=List[dict])
def read_planta(id: int):
    try:
        planta = read_planta_id(id)
        if planta is None:
            raise HTTPException(status_code=404, detail="Planta no trobada")

        return [{"planta": planta}]

    except Exception as e:
        return {"status": -1, "msg": f"Error ocurred: {e}"}
# ---------------- /SELECT PLANTES ----------------

# ---------------- CREATE PLANTES ----------------

# ---------------- /CREATE PLANTES ----------------


# ---------------- UPDATE PLANTES----------------

# ---------------- /UPDATE PLANTES ----------------



# --------------------------------- /PLANTES ---------------------------------

# --------------------------------- USUARIS ---------------------------------
# ---------------- SELECT USUARIS ----------------

# Mostrem tots els Usuaris
@app.get("/usuaris")
def llegir_usuaris():
    usuaris = get_usuaris()
    return {"usuaris": usuaris}


# # Mostrem els Usuaris per id
@app.get("/usuaris/{usuari_id}")
def get_usuari_id(usuari_id: int):
    usuari = read_usuari_id(usuari_id)

    if usuari is None:
        return {"error": f"No s'ha trobat cap usuari amb ID {usuari_id}"}, 404
    elif isinstance(usuari, dict) and usuari.get("status") == -1:
        return {"error": usuari["message"]}, 500

    return {"usuari": usuari}
# ---------------- /SELECT USUARIS ----------------


# ----------------  CREATE USUARIS ----------------

# ---------------- /CREATE USUARIS ----------------

# ---------------- UPDATE USUARIS ----------------

# ---------------- /UPDATE USUARIS ----------------


# --------------------------------- /USUARIS ---------------------------------

# --------------------------------- SENSORS ---------------------------------
# # Mostrem els sensors (?) - hauria de ser productes
# @app.get("/sensors")
# def get_sensors():
#     sensors = read_sensors()
#
#     if isinstance(sensors, dict) and sensors.get("status") == -1:
#         return {"error": sensors["message"]}
#
#     return {"sensors": sensors}
#
# # Mostro els Sensors per id
# @app.get("/sensors/{sensor_id}")
# def get_sensor_id(sensor_id: int):
#     sensor = read_sensors_id(sensor_id)
#
#     if sensor is None:
#         return {"error": f"No s'ha trobat cap sensor amb ID {sensor_id}"}, 404
#     elif isinstance(sensor, dict) and sensor.get("status") == -1:
#         return {"error": sensor["message"]}, 500
#
#     return {"sensor": sensor}

# ----------------  CREATE SENSORS ----------------

# ---------------- /CREATE SENSORS ----------------

# ---------------- UPDATE SENSORS ----------------

# ---------------- /UPDATE SENSORS ----------------

# --------------------------------- /SENSORS ---------------------------------


# --------------------------------- HUMITATS ---------------------------------
# ---------------- SELECT HUMITATS ----------------
# Mostro totes les humitats
@app.get("/humitats")
def llegir_humitats():
    humitats = get_humitat()
    return {"humitats": humitats}


# Mostro les humitats i valor
@app.get("/humitats/valor")
def llegir_valors_humitat():
    valors = db_plantes.get_valors_humitat()
    return {"valors": valors}

# Mostro les humitats per la seva id
@app.get("/humitat/{id}")
def get_humitat_sol_id(id: int):
    humitat = read_humitatSol_id(id)

    if humitat is None:
        return {"error": f"No s'ha trobat humitat amb ID {id}"}, 404
    elif isinstance(humitat, dict) and humitat.get("status") == -1:
        return {"error": humitat["message"]}, 500

    return {"humitat": humitat}
# ---------------- /SELECT HUMITATS ----------------
# --------------------------------- /HUMITATS ---------------------------------

# --------------------------------- POST ---------------------------------
# -------------------------------- DELETE---------------------------------
# -------------------------------- UPDATE --------------------------------