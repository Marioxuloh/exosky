from dotenv import load_dotenv
from astroquery.gaia import Gaia

import os


def get_star_details(designation):
    star_details_query = os.getenv('STAR_DETAILS_QUERY')

    # Consulta a la base de datos de Gaia
    query = star_details_query.format(designation)
    job = Gaia.launch_job(query)
    result = job.get_results()

    # Extracción de la posición
    ra = result['ra'][0]  # Ascensión recta
    dec = result['dec'][0]  # Declinación

    # Extracción de la paralaje
    parallax = result['parallax'][0]  # en milisegundos de arco

    print(f"Posición de la estrella: RA = {ra}, Dec = {dec}")
    print(f"Distancia a la estrella: {parallax} parallax")

    return ra, dec, parallax


# Test Script
if __name__ == "__main__":
    load_dotenv()
    get_star_details('Gaia DR2 1693159194226600192')