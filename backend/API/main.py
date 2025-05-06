from fastapi import FastAPI, HTTPException
from db_plantes import db_client
from pydantic import BaseModel

# Importo les querys
from db_plantes import read_plantes, read_planta_id
from db_plantes import read_usuaris, read_usuari_id
from db_plantes import read_sensors, read_sensors_id
from db_plantes import read_humitatSol, read_humitatSol_id

app = FastAPI()

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

# Llegim totes les plantes
@app.get("/plantes")
def get_plantes():
    plantes = read_plantes()

    # Condicional que ens serveix per controlar errors
    if isinstance(plantes, dict) and plantes.get("status") == -1:
        return {"error": plantes["message"]}

    return {"plantes": plantes}

# Llegim UNA planta en concret, agafem l'id
@app.get("/plantes/{planta_id}")
def get_planta_id(planta_id: int):
    planta = read_planta_id(planta_id)

    if planta is None:
        return {"error": f"No s'ha trobat cap planta amb ID {planta_id}"}, 404
    elif isinstance(planta, dict) and planta.get("status") == -1:
        return {"error": planta["message"]}, 500

    return {"planta": planta}

# Mostrem tots els Usuaris
@app.get("/usuaris")
def get_usuaris():
    usuaris = read_usuaris()

    if isinstance(usuaris, dict) and usuaris.get("status") == -1:
        return {"error": usuaris["message"]}

    return {"usuaris": usuaris}

# Mostrem els Usuaris per id
@app.get("/usuaris/{usuari_id}")
def get_usuari_id(usuari_id: int):
    usuari = read_usuari_id(usuari_id)

    if usuari is None:
        return {"error": f"No s'ha trobat cap usuari amb ID {usuari_id}"}, 404
    elif isinstance(usuari, dict) and usuari.get("status") == -1:
        return {"error": usuari["message"]}, 500

    return {"usuari": usuari}


# Mostrem els sensors (?) - hauria de ser productes
@app.get("/sensors")
def get_sensors():
    sensors = read_sensors()

    if isinstance(sensors, dict) and sensors.get("status") == -1:
        return {"error": sensors["message"]}

    return {"sensors": sensors}

# Mostro els Sensors per id
@app.get("/sensors/{sensor_id}")
def get_sensor_id(sensor_id: int):
    sensor = read_sensors_id(sensor_id)

    if sensor is None:
        return {"error": f"No s'ha trobat cap sensor amb ID {sensor_id}"}, 404
    elif isinstance(sensor, dict) and sensor.get("status") == -1:
        return {"error": sensor["message"]}, 500

    return {"sensor": sensor}

# Mostro totes les humitats
@app.get("/humitats")
def get_humitats():
    humitat = read_humitatSol()

    if humitat is None:
        return {"error": f"No s'ha trobat cap humitat registrada"}, 404
    elif isinstance(humitat, dict) and humitat.get("status") == -1:
        return {"error": humitat["message"]}, 500

    return {"humitat":humitat}

# Mostro les humitats per la seva id
@app.get("/humitat-sol/{humitat_id}")
def get_humitat_sol_id(humitat_id: int):
    humitat = read_humitatSol_id(humitat_id)

    if humitat is None:
        return {"error": f"No s'ha trobat humitat amb ID {humitat_id}"}, 404
    elif isinstance(humitat, dict) and humitat.get("status") == -1:
        return {"error": humitat["message"]}, 500

    return {"humitat": humitat}