from django.db import models
from users.models import User
from exoplanets.models import Exoplanet

class Constellation(models.Model):
    exoplanet = models.ForeignKey(Exoplanet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coordenates = models.JSONField()

    def __str__(self):
        return f"{self.user.name} - {self.exoplanet.pl_name}"
