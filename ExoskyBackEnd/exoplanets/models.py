from django.db import models

class Exoplanet(models.Model):
    pl_name = models.CharField(max_length=150, unique=True)
    hostname = models.CharField(max_length=150)
    gaia_id = models.CharField(max_length=150)
    ra = models.FloatField()
    dec = models.FloatField()
    sy_dist = models.FloatField()
    disc_year = models.IntegerField()
    discoverymethod = models.CharField(max_length=150)
    disc_facility = models.CharField(max_length=150)

    def __str__(self):
        return self.pl_name