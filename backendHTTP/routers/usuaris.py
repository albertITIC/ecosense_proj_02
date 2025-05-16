from typing import Dict, List

# Funció per transformar un usuari individual
def usuari_schema(usuari: Dict) -> Dict:
    return {
        "id": usuari["id"],
        "nom": usuari["nom"],
        "cognom": usuari["cognom"]  ,
        "email": usuari["email"],
        # "contrasenya": usuari["contrasenya"],
        "sensor_id": usuari["sensor_id"],
    }

# Funció per transformar una llista d’usuaris
def usuaris_schema(usuaris: List) -> List:
    return [usuari_schema(u) for u in usuaris]