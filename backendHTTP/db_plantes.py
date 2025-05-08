from client import get_json_data

def get_plantes_by_usuari(usuari_id: int):
    dades = get_json_data()
    if dades.get("status") == -1:
        return dades

    usuaris = dades.get("usuaris", [])
    plantes = dades.get("planta", [])

    usuari = next((u for u in usuaris if u["id"] == usuari_id), None)
    if usuari is None:
        return {"status": -1, "msg": "Usuari no trobat"}

    sensor_id = usuari.get("sensor_id")
    plantes_usuari = [p for p in plantes if p["sensor_id"] == sensor_id]

    return plantes_usuari