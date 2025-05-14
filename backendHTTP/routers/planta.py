# Funció per transformar una planta (diccionari) a un format concret
def planta_schema(planta: dict) -> dict:
    return {
        "id": planta["id"],
        "nom": planta["nom"],
        "sensor_id": planta["sensor_id"]
    }

# Funció per transformar una llista de plantes
def plantes_schema(plantes: list) -> list:
    return [planta_schema(p) for p in plantes]
