from dotenv import load_dotenv

import requests
import os

def get_exoplanets_data():
    url_exoplanets = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync'
    query_all_exoplanets_name = "SELECT pl_name, hostname, gaia_id, ra, dec, sy_dist, disc_year, discoverymethod, disc_facility FROM ps"

    # Parámetros de la solicitud
    params = {
        "query": query_all_exoplanets_name,
        "format": "json"
    }

    # Realizar la solicitud a la API
    response = requests.get(url_exoplanets, params=params)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener los datos en formato JSON
        return response.json()
    else:
        return {"error": "No se pudo obtener la data de Exoplanet Archive"}


#Test script
if __name__ == "__main__":
    load_dotenv()
    print(get_exoplanets_data())