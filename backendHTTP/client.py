import requests

# Funció per fer la petició GET al servidor remot
def get_json_data():
    try:
        url = "http://18.213.199.248:5000/consultar_dades"  # Aquí poses l'URL real
        response = requests.get(url)
        response.raise_for_status()  # Llença error si el codi de resposta és 4xx o 5xx
        return response.json()
    except Exception as e:
        return {"status": -1, "message": str(e)}