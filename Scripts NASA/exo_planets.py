from dotenv import load_dotenv

import requests
import os


def get_explanets():
    url_exoplanets = os.getenv('EXOPLANETS_URL')
    query_all_exoplanets_name = os.getenv('ALL_EXOPLANETS_QUERY')

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
        exoplanets = response.json()
        # Imprimir la lista de exoplanetas

        print(len(exoplanets))

        return exoplanets
    else:
        print("Error en la solicitud:", response.status_code)


#Test script
if __name__ == "__main__":
    load_dotenv()
    print(get_explanets())