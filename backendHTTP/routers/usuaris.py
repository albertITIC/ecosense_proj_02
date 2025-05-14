# Funció per transformar un usuari individual
def usuari_schema(usuari: dict) -> dict:
    return {
        "id": usuari["id"],
        "nom": usuari["nom"],
        "cognom": usuari["cognom"],
        "email": usuari["email"],
        "contrasenya": usuari["contrasenya"]
    }

# Funció per transformar una llista d’usuaris
def usuaris_schema(usuaris: list) -> list:
    return [usuari_schema(u) for u in usuaris]
