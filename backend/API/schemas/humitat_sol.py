# Fitxer que controla la Taula de lectures d'humitat del sòl
def humitat_sol_schema(lectura) -> dict:
    return {
        "id": lectura[0],
        "sensor_id": lectura[1],
        "valor": lectura[2],
        "timestamp": lectura[3]
    }

# Recorrem les dades
def humitats_sol_schema(lectures) -> list:
    return [humitat_sol_schema(l) for l in lectures]