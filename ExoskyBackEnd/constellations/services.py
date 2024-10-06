from .models import Constellation
from exoplanets.models import Exoplanet
from users.models import User

def get_constellations(pl_name):
    try:
        # Buscar el exoplaneta por su nombre
        exoplanet = Exoplanet.objects.get(pl_name=pl_name)
        # Obtener las constelaciones relacionadas con este exoplaneta
        constellations = Constellation.objects.filter(exoplanet=exoplanet)

        # Serializar manualmente
        result = []
        for constellation in constellations:
            result.append({
                'id': constellation.id,
                'exoplanet': constellation.exoplanet.pl_name,  # Suponiendo que quieres el nombre
                'user': constellation.user.name,  # Suponiendo que quieres el nombre de usuario
                'coordenates': constellation.coordenates,
            })

        return {
            'result': result
        }

    except Exoplanet.DoesNotExist:
        return {"error": "Exoplanet not found."}

def insert_constellation(user_name, exoplanet_name, constellation):
    planet = User.objects.get(name=user_name)
    constellation_entity = Constellation(
        user=User.objects.get(name=user_name),
        exoplanet=Exoplanet.objects.get(pl_name=exoplanet_name),
        coordenates=constellation,
    )
    constellation_entity.save()
    return "insertado exitosamente"