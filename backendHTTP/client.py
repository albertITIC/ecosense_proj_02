# Fa la petició al servidor intermediari
# client.py
import requests

def get_json_data():
    try:
        url = "http://18.213.199.248:5000/consultar_dades"
        response = requests.get(url)
        response.raise_for_status()  # Llença error si l'estat no és 200
        return response.json()
    except requests.RequestException as e:
        return {"status": -1, "msg": f"Error en la petición: {e}"}
