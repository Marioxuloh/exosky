import matplotlib.pyplot as plt

import gaia.services as gaia
import transversal.utils as utils

import pandas as pd

def show_3d_space(stars, title):
    # Crear el gráfico
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(stars['X'], stars['Y'], stars['Z'], c="y", s=1)
    
    ax.scatter(0, 0, 0, c='b', s=5)

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Mostrar el gráfico
    plt.show()

def show_3d_space_delete(stars, starsDelete, title):
    # Crear el gráfico
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(stars['X_sphere'], stars['Y_sphere'], stars['Z_sphere'], c="y", s=1)
    ax.scatter(starsDelete['X_sphere'], starsDelete['Y_sphere'], starsDelete['Z_sphere'], c="r", s=1)
    ax.scatter(0, 0, 0, c='b', s=5)

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Mostrar el gráfico
    plt.show()

# Mostrar nube de puntos, se debe tener en cuenta ingresar 3 listas con la misma dimensión
def show_3d_space_sphere(stars, title):
    # Crear el gráfico
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(stars['X_sphere'], stars['Y_sphere'], stars['Z_sphere'], c="y", s=1)
    
    ax.scatter(0, 0, 0, c='b', s=5)

    # Etiquetas de los ejes
    ax.set_xlabel('X - ly')
    ax.set_ylabel('Y - ly')
    ax.set_zlabel('Z - ly')
    ax.set_title(title)

    # Mostrar el gráfico
    plt.show()


##############################################################################################################################
n_stars = 5000
visible_distance = 100

result = gaia.get_star_details("Gaia DR2 1693159194226600192")
# result = gaia.get_star_details("Gaia DR2 5853498713160606720")

ra = result['ra']
dec = result['dec']
parallax = result['parallax']
phot_g_mean_mag = result['phot_g_mean_mag']

# ra = 0
# dec = 0
# parallax = 768.5003653333918
# phot_g_mean_mag = 

parsecs = utils.parallaxmas_to_parsec(parallax)

pointX, pointY, pointZ = utils.convert_skypoint_to_cartesian(ra, dec, parsecs)

stars = gaia.get_nearby_stars(ra, dec, parsecs, visible_distance, n_stars)

stars = utils.add_dataframe_xyz(stars)
show_3d_space(stars, f"Stars view from earth {len(stars)}")

starsCenter = utils.change_cartesian_reference_point(pointX, pointY, pointZ, stars)
show_3d_space(starsCenter, f"Translate to exoplanet {len(starsCenter)}")

starsClear = utils.clear_extra_points(starsCenter, utils.light_years_to_parsec(visible_distance))
show_3d_space(starsClear, f"Stars clear {len(starsClear)}")

show_3d_space_delete(starsClear, pd.concat([starsCenter.to_pandas(), starsClear.to_pandas()]).drop_duplicates(keep=False), f"Stars cleared {len(starsClear)}")

starsModeSphere = utils.translate_sphere_mode(starsClear, 100)
show_3d_space_sphere(starsModeSphere, f"Sphere View {len(starsModeSphere)}")

input("...")