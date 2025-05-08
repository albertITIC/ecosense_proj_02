# Fitxer que controla la Taula de lectures d'humitat del sòl
# Converteix una lectura d'humitat en un diccionari
def humitat_sol_schema(lectura: tuple) -> dict:
    return {
        "id": lectura[0],
        "sensor_id": lectura[1],
        "valor": lectura[2],
        "timestamp": lectura[3]  # Format ISO per defecte de PostgreSQL
    }

# Converteix una llista de lectures en una llista de diccionaris
def humitats_sol_schema(lectures: list) -> list:
    return [humitat_sol_schema(l) for l in lectures]
