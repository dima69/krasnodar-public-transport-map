import requests
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer


def get_gps_data():
    r = requests.get('http://marsruty.ru/krasnodar/gps.txt', timeout=2)
    raw_gps_data = r.text
    gps_data = []
    vehicle_types = {"1": "Троллейбус", "2": "Автобус", "3": "Трамвай"}
    for line in raw_gps_data.strip().split('\n'):
        vehicle_type, route, lng, lat, speed, degree, vehicle_id, *other = line.split(',')
        if vehicle_type in ('1', '2', '3'):
            gps_data.append({
                "vehicle_type": vehicle_types.get(vehicle_type),
                "route": route,
                "latitude": float(lat[:2] + '.' + lat[2:]),
                "longitude": float(lng[:2] + '.' + lng[2:]),
                "speed": int(speed) if speed else 0,
                "degree": int(degree) if degree else 0,
                "vehicle_id": vehicle_id
            })
    return gps_data


class VehicleView(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        gps_data = get_gps_data()
        return Response(gps_data)


def index(request):
    return render(request, "index.html")
