from dotenv import load_dotenv

import matplotlib.pyplot as plt

import os
import nearby_stars
import utils
import planetary_system


# Mostrar nube de puntos, se debe tener en cuenta ingresar 3 listas con la misma dimensión
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

# Mostrar nube de puntos, se debe tener en cuenta ingresar 3 listas con la misma dimensión
def show_3d_space_sphere(stars):
    # Crear el gráfico
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(stars['X_sphere'], stars['Y_sphere'], stars['Z_sphere'], c="y", s=1)
    
    ax.scatter(0, 0, 0, c='b', s=5)

    # Etiquetas de los ejes
    ax.set_xlabel('X - ly')
    ax.set_ylabel('Y - ly')
    ax.set_zlabel('Z - ly')

    # Mostrar el gráfico
    plt.show()
    
    
# Test Script
if __name__ == "__main__":
    load_dotenv()
    visible_distance = float(os.getenv('VISIBLE_DISTANCE'))
    
    ra, dec, parallax = planetary_system.get_star_details("Gaia DR2 1693159194226600192")
    #ra, dec, parallax = planetary_system.get_star_details("Gaia DR2 5853498713160606720")
    radius = utils.convert_parsecs_to_angle(utils.light_years_to_parsec(visible_distance), utils.parallaxmas_to_parsec(parallax))
    
    pointX, pointY, pointZ = utils.convert_skypoint_to_cartesian(ra, dec, utils.parallaxmas_to_parsec(parallax))
    
    stars = nearby_stars.get_nearby_stars(ra, dec, parallax, visible_distance, radius)
    stars = utils.add_dataframe_xyz(stars)
    show_3d_space(stars, "stars of earth")
    
    starsCenter = utils.change_cartesian_reference_point(pointX, pointY, pointZ, stars)
    show_3d_space(starsCenter, "Translate to exoplanet")
    
    starsSphere = utils.clear_extra_points(stars, utils.light_years_to_parsec(visible_distance))
    show_3d_space(starsSphere, "stars clear")
    
    starsSphere2 = utils.clear_extra_points2(stars, utils.light_years_to_parsec(visible_distance))
    show_3d_space(starsSphere2, "stars clear / 2")
    
    starsModeSphere = utils.translate_sphere_mode(stars, 1)
    show_3d_space_sphere(starsModeSphere)
    
    input("...")