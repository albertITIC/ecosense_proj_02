from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

# Per usuaris
from db_plantes import get_usuaris, get_usuari_by_id, create_usuari, delete_usuari_by_id, check_credentials, update_usuari, read_plantes_by_usuari_id

# Per plantes
from db_plantes import get_plantes, read_planta_by_id, create_planta, update_planta, delete_planta 
                 
# Per sensors
from db_plantes import get_all_sensors, get_sensor_by_id, create_sensor, update_sensor, delete_sensor

# Per humitat sol
from db_plantes import get_all_humitats, get_humitat_by_id, create_humitat, update_humitat, delete_humitat

from routers.usuaris import usuari_schema, usuaris_schema
from routers.planta import planta_schema, plantes_schema

from client import db_client
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O pots posar ["http://127.0.0.1:5501"] per més seguretat
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BASE MODELS --------------------------------------------------------------
# Humitat_sol
class humitat_sol(BaseModel):
    id: int
    sensor_id: int
    valor: float
    timestamp : int

# Crear una nova humitat --> crec que no fa falta*
class HumitatCreate(BaseModel):
     sensor_id: int
     valor: float

# Planta
class Planta(BaseModel):
    id: int
    nom: str
    ubicacio: str
    sensor_id: int
    usuari_id: Optional[int] = None
    imagen_url: Optional[str] = None
    
# Crear una nova planta
class PlantaCreate(BaseModel):
    nom: str
    ubicacio: str
    sensor_id: int
    usuari_id: Optional[int] = None
    imagen_url: Optional[str] = None

# Sensors
class sensors(BaseModel):
    sensor_id: int
    ubicacio: str
    planta: str
    estat: str

# Crear un nou sensor
class SensorCreate(BaseModel):
    estat: str
    usuari_id: Optional[int] = None

# Crear un nou usuari
class UsuariCreate(BaseModel):
    # id: int -> es autoincremental
    nom: str
    cognom: str
    email: EmailStr
    contrasenya: str
    sensor_id: Optional[int] = None
    
# Fer login per l'usuari
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., alias="gmail") # Per poder utilitzar gmail en comptes de email
    contrasenya: str

# Actualitzar usuari
class UsuariUpdate(BaseModel):
    nom: Optional[str] = None
    cognom: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasenya: Optional[str] = None
    sensor_id: Optional[int] = None

# /BASE MODELS --------------------------------------------------------------
@app.get("/")
def index():
    return {"Missatge": "Benvingut a l'API Ecosense"}

# Comprova que hi hagi connexió
@app.get("/prova-connexio")
def prova_connexio():
    try:
        conn = db_client()
        conn.close()
        return {"connexio": "correcta"}
    except Exception as e:
        return {"error": str(e)}

# -------------------------------------------------------------- USUARI --------------------------------------------------------------   
# Obtenir tots els usuaris
@app.get("/usuaris")
def llegir_usuaris():
    usuaris = get_usuaris()
    return {"usuaris": usuaris_schema(usuaris)}

# Mostro l'usuari    per l'id
@app.get("/usuari/{id_usuari}")
def llegir_usuari(id_usuari: int):
    usuari = get_usuari_by_id(id_usuari)
    if not usuari:
        raise HTTPException(status_code=404, detail="Usuari no trado")
    return usuari_schema(usuari)


# Crear un usuari per l'id
@app.post("/crear_usuari")
def crear_usuari(usuari_data: UsuariCreate):
    result = create_usuari(usuari_data)
    if result["status"] == -1:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )
    return result

# Elimino usuari per l'id
@app.delete("/eliminiar_usuari/{id_usuari}")
def eliminar_usuari(id_usuari: int):
    resultat = delete_usuari_by_id(id_usuari)
    if resultat["status"] == -1:
        raise HTTPException(status_code=404, detail=resultat["message"])
    return resultat

# Actualitzo un usuari per l'id
@app.put("/usuaris/{id_usuari}")
def actualitzar_usuari(id_usuari: int, dades: UsuariUpdate):
    result = update_usuari(id_usuari, dades.dict())

    if isinstance(result, dict) and result.get("status") == -1:
        raise HTTPException(status_code=500, detail=result["message"])

    if result == 0:
        raise HTTPException(status_code=404, detail="Usuari no trobat")

    return {"msg": "Usuari actualitzat correctament"}

# PLANTES x USUARI --------------------------- 
# Mostro les planes que te cada usuari
@app.get("/usuaris/{usuari_id}/plantes", response_model=List[Planta])
def get_plantes_per_usuari(usuari_id: int):
    plantes = read_plantes_by_usuari_id(usuari_id)

    if isinstance(plantes, dict) and plantes.get("status") == -1:
        raise HTTPException(status_code=500, detail=plantes["message"])

    if not plantes:
        raise HTTPException(status_code=404, detail=f"No s'han trobat plantes per l'usuari amb ID {usuari_id}")

    return plantes

# LOGIN:
@app.post("/login")
def login(data: LoginRequest):
    email = data.email
    contrasenya = data.contrasenya

    resultat = check_credentials(email, contrasenya)

    if resultat["status"] == -1:
        raise HTTPException(status_code=401, detail=str(resultat["message"]))

    usuari = resultat["usuari"]
    usuari.pop("contrasenya", None) # Trec la contrasenya

    return {"msg": "Login correcte, benvingut", "usuari": usuari}

# --------------------------------------------------------------  /USUARI --------------------------------------------------------------   


# --------------------------------------------------------------  PLANTES --------------------------------------------------------------   
# Obtenir totes les plantes
@app.get("/plantes", response_model=List[Planta])
def get_all_plantes():
    plantes = get_plantes()

    if isinstance(plantes, dict) and plantes.get("status") == -1:
        raise HTTPException(status_code=500, detail=plantes["message"])

    return plantes

# Obtenir planta per l'id
@app.get("/plantes/{planta_id}", response_model=Planta)
def get_planta_by_id(planta_id: int):
    planta = read_planta_by_id(planta_id)

    if isinstance(planta, dict) and planta.get("status") == -1:
        raise HTTPException(status_code=500, detail=planta["message"])

    if planta is None:
        raise HTTPException(status_code=404, detail="Planta no trobada")

    return planta

# Crear una nova planta
@app.post("/plantes")
def crear_planta(planta_data: PlantaCreate):
    result = create_planta(planta_data)
    if result["status"] == -1:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Elimino una planta per id
@app.delete("/plantes/{planta_id}")
def eliminar_planta(planta_id: int):
    result = delete_planta(planta_id)
    if result["status"] == -1:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

# Actualitza una planta
@app.put("/plantes/{planta_id}")
def modificar_planta(planta_id: int, planta_data: PlantaCreate):
    result = update_planta(planta_id, planta_data)
    if result["status"] == -1:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


# --------------------------------------------------------------  /PLANTES --------------------------------------------------------------   


# --------------------------------------------------------------  SENSORS --------------------------------------------------------------   
# Obtenir tots els sensors
@app.get("/sensors")
def llistar_sensors():
    sensors = get_all_sensors()
    if isinstance(sensors, dict) and sensors.get("status") == -1:
        raise HTTPException(status_code=500, detail=sensors["message"])
    return sensors

# Obtenir el sensor per id 
@app.get("/sensors/{sensor_id}")
def obtenir_sensor(sensor_id: int):
    sensor = get_sensor_by_id(sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor no trobat")
    return sensor

# Crear un nou sensor
@app.post("/sensors")
def crear_sensor(sensor_data: SensorCreate):
    result = create_sensor(sensor_data)
    if result["status"] == -1:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Elimino un sensor per id
@app.delete("/sensors/{sensor_id}")
def eliminar_sensor(sensor_id: int):
    result = delete_sensor(sensor_id)
    if result["status"] == -1:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

# Actualitza un sensor
@app.put("/sensors/{sensor_id}")
def modificar_sensor(sensor_id: int, sensor_data: SensorCreate):
    result = update_sensor(sensor_id, sensor_data)
    if result["status"] == -1:
        raise HTTPException(status_code=404, detail=result["message"])
    return result
# --------------------------------------------------------------  /SENSORS --------------------------------------------------------------   


# --------------------------------------------------------------  HUMITAT SOL --------------------------------------------------------------   
# Obtenir tots les humimtats
@app.get("/humitats")
def llistar_humitats():
    humitats = get_all_humitats()
    if isinstance(humitats, dict) and humitats.get("status") == -1:
        raise HTTPException(status_code=500, detail=humitats["message"])
    return humitats

# Obtenir les humitats per l'id 
@app.get("/humitats/{humitat_id}")
def obtenir_humitat(humitat_id: int):
    humitat = get_humitat_by_id(humitat_id)
    if humitat is None:
        raise HTTPException(status_code=404, detail="Humitat no trobada")
    return humitat

# Crear nova humitat
@app.post("/humitats")
def crear_humitat(humitat_data: HumitatCreate):
    result = create_humitat(humitat_data)
    if result["status"] == -1:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Elimino una humitat per id
@app.delete("/humitats/{humitat_id}")
def eliminar_humitat(humitat_id: int):
    result = delete_humitat(humitat_id)
    if result["status"] == -1:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

# Actualitza un humitat
@app.put("/humitats/{humitat_id}")
def modificar_humitat(humitat_id: int, humitat_data: HumitatCreate):
    result = update_humitat(humitat_id, humitat_data)
    if result["status"] == -1:
        raise HTTPException(status_code=404, detail=result["message"])
    return result
# --------------------------------------------------------------  /HUMITAT SOL--------------------------------------------------------------   