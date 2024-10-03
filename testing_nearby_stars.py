import matplotlib.pyplot as plt

import os
import nearby_stars
import utils
import exo_planets
import planetary_system


# Mostrar nube de puntos, se debe tener en cuenta ingresar 3 listas con la misma dimensión
def show_3d_space(stars):
    # Crear el gráfico
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(stars['X'], stars['Y'], stars['Z'], c="r", s=1)
    
    ax.scatter(0, 0, 0, c='b', s=5)

    # Etiquetas de los ejes
    ax.set_xlabel('X - ly')
    ax.set_ylabel('Y - ly')
    ax.set_zlabel('Z - ly')

    # Mostrar el gráfico
    plt.show()

# Test Script
if __name__ == "__main__":
    visible_distance = float(os.getenv('VISIBLE_DISTANCE'))
    
    ra, dec, parallax = planetary_system.get_star_details("Gaia DR2 5853498713160606720")
    radius = utils.convert_parsecs_to_angle(utils.light_years_to_parsec(visible_distance),utils.parallaxmas_to_parsec(parallax))

    stars = nearby_stars.get_nearby_stars(ra, dec, parallax, visible_distance, radius)
    stars = utils.add_dataframe_xyz(stars)

    pointX, pointY, pointZ = utils.convert_skypoint_to_cartesian(ra, dec, parallax)

    show_3d_space(stars)
    #show_3d_space(utils.change_cartesian_reference_point(pointX, pointY, pointZ, stars))
    
    input("Presiona Enter para cerrar...")  # Esto mantiene el script en espera hasta que se presione Enter