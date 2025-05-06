# Ficher que controla la Taula de planta
def planta_schema(planta) -> dict:
    return {
        "id": planta[0],
        "nom": planta[1],
        "sensor_id": planta[2]
    }
# Recorrem les dades
def plantes_schema(plantes) -> list:
    return [planta_schema(p) for p in plantes]