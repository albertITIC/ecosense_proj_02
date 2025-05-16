from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from MYSQL_db_plantes import (
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

# --- ENDPOINTS ---

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
