from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import transversal.utils as utils
import os

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
    nearby_star_query = "SELECT TOP {} ABS(distance_gspphot - {}) AS dist_central, designation, ra, dec, distance_gspphot, parallax, pseudocolour, phot_g_mean_flux FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec), CIRCLE('ICRS', {}, {}, {})) AND parallax > 0 AND distance_gspphot BETWEEN {} AND {} ORDER BY dist_central"
    
    distanceParsec = utils.light_years_to_parsec(parsecs)
    toleranceMin = parsecs - utils.light_years_to_parsec(visible_distance) if parsecs - utils.light_years_to_parsec(visible_distance) > 0 else 0
    toleranceMax = parsecs + utils.light_years_to_parsec(visible_distance)

    # El radio no puede ser mayor a 90 grados acorde a la información de gai
    if radius > 90:
        radius = 90

    # Consulta a la base de datos de Gaia
    query = nearby_star_query.format(n_stars, distanceParsec, ra, dec, radius, toleranceMin, toleranceMax)

    job = Gaia.launch_job(query)

    return job.get_results()

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