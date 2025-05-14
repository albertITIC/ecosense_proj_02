def sensor_schema(sensor: dict) -> dict:
    return {
        "sensor_id": sensor["sensor_id"],
        "estat": sensor["estat"],
        "usuari_id": sensor["usuari_id"]
    }

# Funció per transformar una llista de sensors
def sensors_schema(sensors: list) -> list:
    return [sensor_schema(s) for s in sensors]