import requests

# URL del endpoint
URL = "http://18.213.199.248:8000"


def get_json_data():
    try:
        # Hacer la petición al servidor
        response = requests.get(URL)

        # Verificar si la respuesta es correcta
        response.raise_for_status()  # Lanza error si el estado no es 200

        # Devolver los datos JSON si la solicitud es exitosa
        return response.json()

    except requests.RequestException as e:
        # Manejo de excepciones en caso de error en la solicitud
        return {"status": -1, "msg": f"Error en la petición: {e}"}


# Prueba de la función (opcional)
if __name__ == "__main__":
    data = get_json_data()
    print(data)
