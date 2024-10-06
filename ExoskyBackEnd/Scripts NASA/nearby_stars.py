from astroquery.gaia import Gaia
from dotenv import load_dotenv
from astropy.coordinates import SkyCoord

import astropy.units as u
import os
import utils


def get_nearby_stars(ra, dec, parallax, visible_distance, radius):
    global temp_stars
    nearby_star_query = os.getenv('NEARBY_STAR_QUERY')
    
    ly = utils.parallaxmas_to_light_years(parallax)
    distanceParsec = utils.light_years_to_parsec(ly)
    toleranceMin = utils.light_years_to_parsec(ly - visible_distance) if ly - visible_distance > 0 else 0
    toleranceMax = utils.light_years_to_parsec(ly + visible_distance)
     
    # El radio no puede ser mayor a 90 grados acorde a la información de gai
    radius = utils.convert_parsecs_to_angle(visible_distance, parsecs)
    if radius > 90:
        radius = 90

    # Consulta a la base de datos de Gaia
    query = nearby_star_query.format(distanceParsec, ra, dec, radius, toleranceMin, toleranceMax)

    job = Gaia.launch_job(query)
    result = job.get_results()

    temp_stars = result
    print(f"Total star in search: {len(result)}")

    return result.to_pandas()

def verify_stars_within_radius(ra_center, dec_center, radius):
    inside = 0
    outside = 0
    
    if radius > 90:
        radius = 90

    center_coord = SkyCoord(ra=ra_center*u.degree, dec=dec_center*u.degree, frame='icrs')

    for star in temp_stars:
        star_coord = SkyCoord(ra=star['ra']*u.degree, dec=star['dec']*u.degree, frame='icrs')
        separation = center_coord.separation(star_coord)
        if separation.degree <= radius:
            inside = inside + 1
        else:
            print(f"Star {star['source_id']} is outside the radius.")
            outside = outside + 1
    
    print(f"Start search: {len(temp_stars)}")
    print(f"Start Inside: {inside}")
    print(f"Start Outside: {outside}")


# Test Script
if __name__ == "__main__":
    load_dotenv()

    temp_stars = []

    #Coordenadas de Proxima Centary inclyendo parallax
    ra = 217.39346574260355
    dec = -62.67618210292382
    parallax = 25
    visible_distance = float(os.getenv('VISIBLE_DISTANCE'))
    radius = utils.convert_parsecs_to_angle(utils.light_years_to_parsec(visible_distance),utils.parallaxmas_to_parsec(parallax))
    
    get_nearby_stars(ra, dec, parallax, visible_distance, radius)
    verify_stars_within_radius(ra, dec, radius)
   