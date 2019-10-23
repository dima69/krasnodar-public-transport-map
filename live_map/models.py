from django.db import models


class Vehicles(models.Model):
    vehicle_type = models.CharField(max_length=10)
    route = models.CharField(max_length=5)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.PositiveSmallIntegerField(default=0)
    degree = models.PositiveSmallIntegerField(default=0)
    vehicle_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        self.prep = f"vehicle_type:{self.vehicle_type} route:{self.route}"
        return self.prep
