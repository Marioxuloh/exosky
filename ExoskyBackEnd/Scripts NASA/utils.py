from astropy.coordinates import SkyCoord

import astropy.units as u
import pandas as pd
import numpy as np
import math

# Paralaje en milisegundos de arco a años luz
def parallaxmas_to_light_years(parallax_mas):
    # Convertir paralaje a segundos de arco
    parallax_arcsec = parallax_mas / 1000

    # Calcular la distancia en parsecs
    parsecs = 1 / parallax_arcsec

    # Convertir la distancia a años luz
    distance_ly = parsecs * 3.26

    return distance_ly

# Años luz a paralaje en milisegundos de arco
def light_years_to_parallaxmas(light_years):
    # Convertir años luz a parsecs
    parsecs = light_years / 3.26
    
    # Calcular el paralaje en arcosegundos
    parallax_arcsec = 1 / parsecs
    
    # Convertir arcosegundos a milisegundos de arco
    parallax_mas = parallax_arcsec * 1000
    
    return parallax_mas

# Convertir años luz en radio para la consulta, la distance debe ser en parallax
def light_years_to_parsec(ly):
    return ly / 3.26

# Convertir años luz en radio para la consulta, la distance debe ser en parallax
def parsec_to_light_year(parsec):
    return parsec * 3.26

# Convertir años luz en radio para la consulta, la distance debe ser en parallax
def parallaxmas_to_parsec(parallax_mas):
    parallax_arcsec = parallax_mas / 1000

    # Calcular la distancia en parsecs
    return 1 / parallax_arcsec

# Convertir años luz en radio para la consulta, la distance debe ser en parallax
def light_years_to_angular_distance(distance_ly):
    parsec = light_years_to_parsec(distance_ly)

    # Calcular la distancia en parsecs
    return 1 / parsec

# Convertir años luz en radio para la consulta, valores en parsecs
def convert_parsecs_to_angle(width, distance):
    # C opuesto
    radio = width / 2
    
    return (radio / distance) * (180 / math.pi)

# Añadir al dataframe las coordenadas cartecianas de un punto
def add_dataframe_xyz(df):    
    # Extrae las coordenadas de las estrellas y calcula las distancias
    ra = df['ra']
    dec = df['dec']
    distance = df['distance_gspphot']

    # Convertir coordenadas esféricas a cartesianas
    x = distance * np.cos(np.deg2rad(dec)) * np.cos(np.deg2rad(ra))
    y = distance * np.cos(np.deg2rad(dec)) * np.sin(np.deg2rad(ra))
    z = distance * np.sin(np.deg2rad(dec))
    
    # Agregar las columnas calculadas al DataFrame
    df['X'] = x
    df['Y'] = y
    df['Z'] = z
    
    return df

def translate_sphere_mode(df, r):
    x, y, z = df['X'], df['Y'], df['Z']

    magnitude = np.sqrt(x**2 + y**2 + z**2)
    x_new = r * (x / magnitude)
    y_new = r * (y / magnitude)
    z_new = r * (z / magnitude)
    
    df['X_sphere'] = x_new
    df['Y_sphere'] = y_new
    df['Z_sphere'] = z_new

    return df


# Añadir al dataframe las coordenadas cartecianas de un punto
def convert_skypoint_to_cartesian(ra, dec, distance):
    # Crear un objeto SkyCoord con las coordenadas RA, Dec y paralaje
    coords = SkyCoord(ra=ra * u.degree,
                      dec=dec * u.degree,
                      distance=distance * u.pc,  # Convertir paralaje a distancia en parsecs
                      frame='icrs')
    
    # Obtener las coordenadas cartesianas en parsecsn
    x = coords.cartesian.x.value
    y = coords.cartesian.y.value
    z = coords.cartesian.z.value
    
    # Agregar las columnas calculadas al DataFrame
    return x, y, z

# Añadir al dataframe las coordenadas cartecianas de un punto
def change_cartesian_reference_point(x, y, z, df):    
    # Agregar las columnas calculadas al DataFrame
    df['X'] = df['X'] - x
    df['Y'] = df['Y'] - y
    df['Z'] = df['Z'] - z
    
    return df

def clear_extra_points(df, parsec):
    # Calculamos la distancia al centro (0, 0, 0)
    distancias = np.sqrt(df['X']**2 + df['Y']**2 + df['Z']**2)

    # Filtramos los puntos que están a 1.5 o menos del centro
    df_filtrado = df[distancias <= parsec]
    
    return df_filtrado

def clear_extra_points2(df, parsec):
    # Calculamos la distancia al centro (0, 0, 0)
    distancias = np.sqrt(df['X']**2 + df['Y']**2 + df['Z']**2)

    # Filtramos los puntos que están a 1.5 o menos del centro
    df_filtrado = df[distancias <= parsec/2]
    
    return df_filtrado

# Test Script
if __name__ == "__main__":    
    parallaxmas = 768.0665391873573
    ly = 4.3
    parsec = 1
    
    print(f"Parallax Mas to Light Year: {parallaxmas} => {parallaxmas_to_light_years(parallaxmas)}")
    print(f"Light Year to Parallax Mas: {ly} => {light_years_to_parallaxmas(ly)}")
    print(f"Light Year to Parsec: {ly} => {light_years_to_parsec(ly)}")
    print(f"Parsec to Light Year: {ly} => {parsec_to_light_year(parsec)}")
    print(f"Parallax Mas to Parsec: {parallaxmas} => {parallaxmas_to_parsec(parallaxmas)}")
    print(f"Convert Parsecs To Angle: {convert_parsecs_to_angle(light_years_to_parsec(10), light_years_to_parsec(10))}")
    print(f"Convert Skypoint To Cartesian: {convert_skypoint_to_cartesian(15, 15, 15)}")
    print(f"Add Dataframe xyz: \n {add_dataframe_xyz(pd.DataFrame({ 'ra': [15], 'dec': [15], 'parallax': [15]}))}")
    print(f"Change Cartesian Reference Point: \n {change_cartesian_reference_point(15, 15, 15, pd.DataFrame({ 'X': [15], 'Y': [15], 'Z': [15]}))}")
    print(f"Translate to sphere: \n {translate_sphere_mode(pd.DataFrame({ 'X': [15], 'Y': [15], 'Z': [15]}), 10)}")
    
    
    
    print(f"{parsec_to_light_year(36165.09)}")
    
    # Distancia angular 0.758139534883721