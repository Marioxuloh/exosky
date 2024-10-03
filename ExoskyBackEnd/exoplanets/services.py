import requests

def get_exoplanets_data():
    url_exoplanets = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync'
    query_all_exoplanets_name = "SELECT pl_name, hostname, gaia_id, ra, dec, glon, glat, sy_dist, sy_snum, sy_pnum, sy_mnum, cb_flag FROM ps"

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
        return {"error": "No se pudo obtener la data de Gaia"}

