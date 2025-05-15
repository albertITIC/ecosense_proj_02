# Ficher que controla la Taula d'usuaris
def usuari_schema(usuari) -> dict:
    return {
        "id": usuari[0],
        "nom": usuari[1],
        "cognom": usuari[2],
        "email": usuari[3],
        "contrasenya": usuari[4],
        "sensor_id": usuari[5]
    }


# Recorrem les dades
def usuaris_schema(usuaris) -> list:
    return [usuari_schema(u) for u in usuaris]