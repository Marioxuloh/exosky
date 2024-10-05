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

def get_nearby_stars(ra, dec, parsecs, visible_distance_ly, n_stars):
    nearby_star_query = "SELECT TOP {} ABS(distance_gspphot - {}) AS dist_central, designation, ra, dec, distance_gspphot, parallax, pseudocolour, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec), CIRCLE('ICRS', POINT({}, {}), {})) AND parallax > 0 AND distance_gspphot BETWEEN {} AND {} ORDER BY dist_central"
    
    visible_distance_parsecs = utils.light_years_to_parsec(visible_distance_ly)
    toleranceMin = parsecs - visible_distance_parsecs if parsecs - visible_distance_parsecs > 0 else 0
    toleranceMax = parsecs + visible_distance_parsecs

    # El radio no puede ser mayor a 90 grados acorde a la información de gai
    radius = utils.convert_parsecs_to_angle(parsecs, visible_distance_parsecs)
    
    if radius > 90:
        radius = 90

    # Consulta a la base de datos de Gaia
    query = nearby_star_query.format(n_stars, parsecs, ra, dec, radius, toleranceMin, toleranceMax)
    job = Gaia.launch_job(query)
    stars = job.get_results()

    pointX, pointY, pointZ = utils.convert_skypoint_to_cartesian(ra, dec, parsecs)

    stars = utils.add_dataframe_xyz(stars)
    starsCenter = utils.change_cartesian_reference_point(pointX, pointY, pointZ, stars)
    starsClear = utils.clear_extra_points(starsCenter, visible_distance_parsecs)
    starsModeSphere = utils.translate_sphere_mode(starsClear, 1)

    return starsModeSphere