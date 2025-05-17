from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from MYSQL_db_plantes import (
    get_usuaris,
    get_usuari_by_id,
    create_usuari,
    delete_usuari_by_id,
    update_usuari,
    get_plantes,
    read_planta_by_id,
    create_planta,
    update_planta,
    delete_planta,
    get_all_sensors,
    get_sensor_by_id,
    get_all_humitats,
    get_humitat_by_id,
)

# url FENG: http://18.213.199.248:8000/docs

app = FastAPI()

class PlantaModel(BaseModel):
    nom: str
    ubicacio: str
    sensor_id: Optional[int]
    usuari_id: int
    imagen_url: Optional[str]

class PlantaUpdateModel(PlantaModel):
    pass

class SensorModel(BaseModel):
    sensor_id: int
    estat: str
    usuari_id: int

class HumitatModel(BaseModel):
    sensor_id: int
    valor: float
    timestamp: str  

class UsuariCreate(BaseModel):
    nom: str
    cognom: str
    email: str
    contrasenya: str
    sensor_id: Optional[int] = None

class UsuariUpdate(BaseModel):
    nom: Optional[str] = None
    cognom: Optional[str] = None
    email: Optional[str] = None
    contrasenya: Optional[str] = None
    sensor_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: str
    contrasenya: str

# --- ENDPOINTS ---

# USUARIS
@app.get("/usuaris")
def llegir_usuaris():
    usuaris = get_usuaris()
    if isinstance(usuaris, dict) and usuaris.get("status") == -1:
        raise HTTPException(status_code=500, detail=usuaris["message"])
    return {"usuaris": usuaris}

# GET: Obtenir un usuari per ID
@app.get("/usuari/{id_usuari}")
def llegir_usuari(id_usuari: int):
    usuari = get_usuari_by_id(id_usuari)
    if not usuari:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return usuari

# POST: Crear un nou usuari
@app.post("/crear_usuari")
def crear_usuari(usuari_data: UsuariCreate):
    resultat = create_usuari(usuari_data)
    if resultat["status"] == -1:
        raise HTTPException(status_code=400, detail=resultat["message"])
    return resultat

# DELETE: Eliminar un usuari per ID
@app.delete("/eliminar_usuari/{id_usuari}")
def eliminar_usuari(id_usuari: int):
    resultat = delete_usuari_by_id(id_usuari)
    if resultat["status"] == -1:
        raise HTTPException(status_code=404, detail=resultat["message"])
    return resultat

# PUT: Actualitzar un usuari per ID
@app.put("/usuaris/{id_usuari}")
def actualitzar_usuari(id_usuari: int, dades: UsuariUpdate):
    result = update_usuari(id_usuari, dades.dict())
    if isinstance(result, dict) and result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    if result == 0:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return {"msg": "Usuari actualitzat correctament"}

# LOGIN
@app.post("/login")
def login(data: LoginRequest):
    resultat = check_credentials(data.email, data.contrasenya)
    if resultat["status"] == -1:
        raise HTTPException(status_code=401, detail=str(resultat["message"]))
    return {"msg": "Login correcte", "usuari": resultat["usuari"]}


# PLANTES
@app.get("/plantes", response_model=List[dict])
def api_get_plantes():
    plantes = get_plantes()
    if isinstance(plantes, dict) and plantes.get("status") == -1:
        raise HTTPException(status_code=500, detail=plantes["message"])
    return plantes

@app.get("/plantes/{planta_id}", response_model=dict)
def api_get_planta(planta_id: int):
    planta = read_planta_by_id(planta_id)
    if planta is None:
        raise HTTPException(status_code=404, detail="Planta no trobada")
    if isinstance(planta, dict) and planta.get("status") == -1:
        raise HTTPException(status_code=500, detail=planta["message"])
    return planta

@app.post("/plantes", response_model=dict)
def api_create_planta(planta: PlantaModel):
    result = create_planta(planta)
    if result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.put("/plantes/{planta_id}", response_model=dict)
def api_update_planta(planta_id: int, planta: PlantaUpdateModel):
    result = update_planta(planta_id, planta)
    if result.get("status") == -1:
        raise HTTPException(status_code=404 if "no s'ha trobat" in result["message"].lower() else 500, detail=result["message"])
    return result

@app.delete("/plantes/{planta_id}", response_model=dict)
def api_delete_planta(planta_id: int):
    result = delete_planta(planta_id)
    if result.get("status") == -1:
        raise HTTPException(status_code=404 if "no trobada" in result["message"].lower() else 500, detail=result["message"])
    return result


# SENSORS

@app.get("/sensors", response_model=List[dict])
def api_get_sensors():
    sensors = get_all_sensors()
    if isinstance(sensors, dict) and sensors.get("status") == -1:
        raise HTTPException(status_code=500, detail=sensors["message"])
    return sensors

@app.get("/sensors/{sensor_id}", response_model=dict)
def api_get_sensor(sensor_id: int):
    sensor = get_sensor_by_id(sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor no trobat")
    if isinstance(sensor, dict) and sensor.get("status") == -1:
        raise HTTPException(status_code=500, detail=sensor["message"])
    return sensor


# HUMITATS

@app.get("/humitats", response_model=List[dict])
def api_get_humitats():
    humitats = get_all_humitats()
    if isinstance(humitats, dict) and humitats.get("status") == -1:
        raise HTTPException(status_code=500, detail=humitats["message"])
    return humitats

@app.get("/humitats/{humitat_id}", response_model=dict)
def api_get_humitat(humitat_id: int):
    humitat = get_humitat_by_id(humitat_id)
    if humitat is None:
        raise HTTPException(status_code=404, detail="Humitat no trobada")
    if isinstance(humitat, dict) and humitat.get("status") == -1:
        raise HTTPException(status_code=500, detail=humitat["message"])
    return humitat
