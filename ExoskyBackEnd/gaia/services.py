import requests
import astropy.units as u
from astroquery.gaia import Gaia
import transversal.utils as utils
import pandas as pd
import numpy as np
import json

def get_star_details(designation):
    star_details_query = "SELECT * FROM gaiadr2.gaia_source WHERE designation = '{}'"

    # Consulta a la base de datos de Gaia con astroquery
    query = star_details_query.format(designation)
    job = Gaia.launch_job(query)
    result = job.get_results()
    star_data = {
        "designation": result['DESIGNATION'][0],    # Designation id
        "ra": result['ra'][0],                      # Ascensión recta
        "dec": result['dec'][0],                    # Declinación
        "parallax": result['parallax'][0]           # Paralaje
    }

    return star_data

def get_nearby_stars(ra, dec, parsecs, visible_distance, n_stars):
    global temp_stars
    nearby_star_query = "SELECT TOP {} * FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec), CIRCLE('ICRS', {}, {}, {})) AND parallax > 0 AND distance_gspphot BETWEEN {} AND {} ORDER BY distance_gspphot DESC"
    
    toleranceMin = parsecs - utils.light_years_to_parsec(visible_distance) if parsecs - utils.light_years_to_parsec(visible_distance) > 0 else 0
    toleranceMax = utils.light_years_to_parsec(visible_distance) + parsecs
    radius = utils.convert_parsecs_to_angle(utils.light_years_to_parsec(visible_distance), parsecs)
  
    # El radio no puede ser mayor a 90 grados acorde a la información de gai
    if radius > 90:
        radius = 90

    # Consulta a la base de datos de Gaia
    query = nearby_star_query.format(n_stars ,ra, dec, radius, toleranceMin, toleranceMax)
    job = Gaia.launch_job(query)

    return job.get_results()