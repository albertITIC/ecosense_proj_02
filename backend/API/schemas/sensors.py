# Ficher que controla la Taula Sensors
def sensor_schema(sensor) -> dict:
    return {
        "sensor_id": sensor[0],
        "ubicacio": sensor[1],
        "planta": sensor[2],
        "estat": sensor[3]
    }
# Recorrem les dades
def sensors_schema(sensors) -> list:
    return [sensor_schema(s) for s in sensors]