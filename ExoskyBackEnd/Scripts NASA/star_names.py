from astroquery.simbad import Simbad


def get_star_name(gaiaRD2):
    # Configurar Simbad para buscar por designación
    custom_simbad = Simbad()
    custom_simbad.add_votable_fields('ids')

    result_table = custom_simbad.query_object(gaiaRD2)

    if result_table is None:
        return gaiaRD2

    # Obtener el nombre común
    nombres = result_table['IDS'][0].decode('utf-8').split('|')
    nombre_comun = nombres[0] if nombres else gaiaRD2

    return nombre_comun

# Test Script
if __name__ == "__main__":
    get_star_name("")