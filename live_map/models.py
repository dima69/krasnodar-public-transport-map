from django.db import models


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        (1, 'Троллейбус'),
        (2, 'Автобус'),
        (3, 'Трамвай')
    ]
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    route = models.CharField(max_length=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.PositiveSmallIntegerField(default=0)
    azimuth = models.PositiveSmallIntegerField(default=0)
    vehicle_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        self.prep = f"route:{self.route} type:{self.vehicle_type} id:{self.vehicle_id}"
        return self.prep
