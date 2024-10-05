from astroquery.simbad import Simbad


def get_star_name(gaiaRD2):
    # Configurar Simbad para buscar por designación
    custom_simbad = Simbad()
    custom_simbad.add_votable_fields('ids')

    result_table = custom_simbad.query_object(gaiaRD2)

    if result_table is None:
        return gaiaRD2

    # Obtener el nombre común
    nombre = result_table['MAIN_ID'][0].split('NAME')[-1].strip()

    return nombre

# Test Script
if __name__ == "__main__":
    print(get_star_name("Gaia DR2 5853498713160606720"))
    print(get_star_name("Gaia DR2 1693159194226600192"))