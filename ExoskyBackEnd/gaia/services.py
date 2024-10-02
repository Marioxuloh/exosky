import requests

def get_gaia_data():
    url = "https://api.gaia.example.com/data"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "No se pudo obtener la data de Gaia"}
