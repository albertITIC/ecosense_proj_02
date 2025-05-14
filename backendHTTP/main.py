from fastapi import FastAPI
# Funcions/ querys
from db_plantes import get_plantes_by_usuari, get_all_sensors

# Esquemas
from routers.planta import plantes_schema
from routers.sensors import sensors_schema

app = FastAPI()


@app.get("/")
def index():
    return {"Missatge": "Benvingut a l'API Ecosense"}

@app.get("/usuaris/{usuari_id}/plantes")
def plantes_per_usuari(usuari_id: int):
    dades = get_plantes_by_usuari(usuari_id)
    return plantes_schema(dades)

# Per obtenir tots els sensors
@app.get("/sensors")
def llistar_sensors():
    dades = get_all_sensors()
    return sensors_schema(dades)
