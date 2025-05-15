from client import get_json_data

# Funció per obtenir totes les plantes associades a un usuari
def get_plantes_by_usuari(usuari_id: int):
    dades = get_json_data()

    if dades.get("status") == -1:
        return dades

    plantes = dades.get("planta", [])

    # Filtrar les plantes que tenen el camp usuari_id igual al que es busca
    plantes_usuari = [planta for planta in plantes if planta.get("usuari_id") == usuari_id]

    return plantes_usuari

# Fució per obtenir tots els sensors
from client import get_json_data

def get_all_sensors():
    dades = get_json_data()
    
    if dades.get("status") == -1:
        return dades

    return dades.get("sensors", [])



# Test
from client import get_json_data

# Funció que retorna les plantes per usuari
def get_plantes_by_usuari(usuari_id: int):
    dades = get_json_data()
    if dades.get("status") == -1:
        return dades

    plantes = dades.get("planta", [])
    return [p for p in plantes if p.get("usuari_id") == usuari_id]

