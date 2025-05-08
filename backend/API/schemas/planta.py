# Ficher que controla la Taula de planta
def planta_schema(planta) -> dict:
    return {
        "id": planta["id"],
        "nom": planta["nom"],
        "sensor_id": planta["sensor_id"]
    }

def plantes_schema(plantes) -> list:
    return [planta_schema(p) for p in plantes]