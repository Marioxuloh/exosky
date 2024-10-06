from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import transversal.utils as utils
import math
import numpy as np

def get_star_details(designation):
    star_details_query = "SELECT * FROM gaiadr2.gaia_source WHERE designation = '{}'"

    # Consulta a la base de datos de Gaia con astroquery
    query = star_details_query.format(designation)
    job = Gaia.launch_job(query)
    result = job.get_results()
    star_data = {
        "designation": result['DESIGNATION'][0],        # Designation id
        "ra": result['ra'][0],                          # Ascensión recta
        "dec": result['dec'][0],                        # Declinación
        "parallax": result['parallax'][0],              # Paralaje
        "phot_g_mean_mag": result['phot_g_mean_mag'][0] # Paralaje
    }

    return star_data

def get_nearby_stars(ra, dec, parsecs, visible_distance_ly, n_stars):
    nearby_star_query = "SELECT TOP {} ABS(distance_gspphot - {}) AS dist_central, designation, ra, dec, distance_gspphot, parallax, pseudocolour, phot_g_mean_mag, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux, bp_rp FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS', gaiadr3.gaia_source.ra, gaiadr3.gaia_source.dec), CIRCLE('ICRS', POINT({}, {}), {})) AND parallax > 0 AND distance_gspphot BETWEEN {} AND {} ORDER BY dist_central"
    
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
    starsModeSphere = utils.translate_sphere_mode(starsClear, 100)
    starsModeSphereWhitoutHighAparentMag = starsModeSphereWhitoutHighAparentMagFunc(starsModeSphere)
    starsModeSphereWhitRGB = starsModeSphereWhitRGBFunc(starsModeSphereWhitoutHighAparentMag)

    return starsModeSphereWhitRGB

############## scripts ##############

def starsModeSphereWhitoutHighAparentMagFunc(starsModeSphere):
    min_value_view = 10

    phot_g_mean_mag = starsModeSphere['phot_g_mean_mag']
    distance_gspphot = starsModeSphere['distance_gspphot']
    distance_gspphot_exoplanet = starsModeSphere['distance_gspphot_exoplanet']

    absolute_mag_star = absolute_mag(phot_g_mean_mag, distance_gspphot)
    aparent_mag_exoplanet = aparent_mag_from_exoplanet(absolute_mag_star, distance_gspphot_exoplanet)

    starsModeSphere['aparent_mag_exoplanet'] = aparent_mag_exoplanet
    
    starsModeSphere['radius_sphere'] = (starsModeSphere['aparent_mag_exoplanet'] * 0.5) / 5

    return starsModeSphere[starsModeSphere['aparent_mag_exoplanet'] < min_value_view]

def starsModeSphereWhitRGBFunc(starsModeSphereWhitoutHighAparentMag):
    ## bp_rp
    bp_rp = starsModeSphereWhitoutHighAparentMag['bp_rp']
    kelvin = bp_rp_to_kelvin(bp_rp)
    r, g, b = kelvin_to_rgb(kelvin)
    starsModeSphereWhitoutHighAparentMag['kelvin_aprox_max9'] = kelvin
    starsModeSphereWhitoutHighAparentMag['color_r'] = r
    starsModeSphereWhitoutHighAparentMag['color_g'] = g
    starsModeSphereWhitoutHighAparentMag['color_b'] = b
    return starsModeSphereWhitoutHighAparentMag

def absolute_mag(phot_g_mean_mag, distance_gspphot):
    absolute_mag = phot_g_mean_mag - (5 * np.log10(distance_gspphot)) + 5
    return absolute_mag

def aparent_mag_from_exoplanet(absolute_mag, distance_from_exoplanet):
    aparent_mag = absolute_mag + (5 * np.log10(distance_from_exoplanet)) - 5
    return aparent_mag

def bp_rp_to_kelvin(bp_rp):
    bp_rp = np.asarray(bp_rp)
    kelvin = 4600 * (1 / (bp_rp + 0.92)) + 4000
    return kelvin

def kelvin_to_rgb(kelvin):
    # Ensure temperature is within the valid range for visible colors
    kelvin = np.clip(kelvin, 1000, 40000)
    kelvin /= 100.0

    # RED
    r = np.where(kelvin <= 66, 255, 329.698727446 * (kelvin - 60) ** -0.1332047592)
    r = np.clip(r, 0, 255)

    # GREEN
    g = np.where(kelvin <= 66, 99.4708025861 * np.log(kelvin) - 161.1195681661,
                 288.1221695283 * (kelvin - 60) ** -0.0755148492)
    g = np.clip(g, 0, 255)

    # BLUE
    b = np.where(kelvin >= 66, 255, np.where(kelvin <= 19, 0,
                                           138.5177312231 * np.log(kelvin - 10) - 305.0447927307))
    b = np.clip(b, 0, 255)

    return r.astype(int), g.astype(int), b.astype(int)