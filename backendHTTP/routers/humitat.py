# Funció per transformar una lectura de humitat
def humitat_schema(humitat: dict) -> dict:
    return {
        "id": humitat["id"],
        "sensor_id": humitat["sensor_id"],
        "valor": humitat["valor"],
        "timestamp": humitat["timestamp"]
    }

# Funció per transformar una llista de lectures
def humitats_schema(humitats: list) -> list:
    return [humitat_schema(h) for h in humitats]