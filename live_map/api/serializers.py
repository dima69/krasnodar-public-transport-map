from rest_framework import serializers

from live_map.models import Vehicles


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = "vehicle_type", "route", "lat", "lng", "speed", "degree", "vehicle_id"
