import requests
import json
from .models import Exoplanet
import os
from django.db import IntegrityError


def save_exoplanets_data():
    url_exoplanets = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync'

    query_all_exoplanets_name = "SELECT pl_name, hostname, gaia_id, ra, dec, sy_dist, disc_year, discoverymethod, disc_facility FROM ps WHERE gaia_id IS NOT NULL AND ra IS NOT NULL AND dec IS NOT NULL AND sy_dist IS NOT NULL"

    # Parámetros de la solicitud
    params = {
        "query": query_all_exoplanets_name,
        "format": "json"
    }

    # Realizar la solicitud a la API
    response = requests.get(url_exoplanets, params=params)

    planets = response.json()

    # Crear instancias de Exoplanet y guardarlas en la base de datos
    for planet_data in planets:
        exoplanet = Exoplanet(
            pl_name=planet_data['pl_name'],
            hostname=planet_data['hostname'],
            gaia_id=planet_data['gaia_id'],
            ra=planet_data['ra'],
            dec=planet_data['dec'],
            sy_dist=planet_data['sy_dist'],
            disc_year=planet_data['disc_year'],
            discoverymethod=planet_data['discoverymethod'],
            disc_facility=planet_data['disc_facility']
        )
        
        try:
            exoplanet.save()  # Intenta guardar el exoplaneta
            print(f'Inserted new exoplanet: {exoplanet.pl_name}')  # Mensaje de éxito
        except IntegrityError:
            print(f'Exoplanet already exists: {exoplanet.pl_name}')  # Mensaje si ya existe


    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener los datos en formato JSON
        return planets
    else:
        return {"error": "No se pudo obtener la data de Exoplanet Archive"}

def get_exoplanets_data():
    # get exoplanets from db
    exoplanets = Exoplanet.objects.all()
    return list(exoplanets.values('pl_name', 'hostname', 'gaia_id', 'ra', 'dec', 'sy_dist', 'disc_year', 'discoverymethod', 'disc_facility'))

def get_random_exoplanets_data(limit):
    exoplanets = Exoplanet.objects.order_by('?')[:limit]
    return list(exoplanets.values('pl_name', 'hostname', 'gaia_id', 'ra', 'dec', 'sy_dist', 'disc_year', 'discoverymethod', 'disc_facility'))

def get_exoplanets_by_id(pl_name):
    try:
        exoplanet = Exoplanet.objects.filter(pl_name=pl_name).values('pl_name', 'hostname', 'gaia_id', 'ra', 'dec', 'sy_dist', 'disc_year', 'discoverymethod', 'disc_facility').first()
        return exoplanet
    except Exception as e:
        print(f"Error: {e}")
        return None