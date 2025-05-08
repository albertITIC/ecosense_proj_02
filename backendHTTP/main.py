# Punto de entrada de la API
from fastapi import FastAPI
from db_plantes import get_plantes_by_usuari
from plantes import plantes_schema

app = FastAPI()

# Ruta principal
@app.get("/")
def index():
    return {"Missatge": "Benvingut a l'API Ecosense"}

# Ruta per obtenir les plantes d’un usuari concret
@app.get("/usuaris/{usuari_id}/plantes")
def plantes_per_usuari(usuari_id: int):
    dades = get_plantes_by_usuari(usuari_id)
    return plantes_schema(dades)
