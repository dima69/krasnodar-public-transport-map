from django.urls import path

from live_map.views import index_gis, index_leaflet
from live_map.api.views import VehicleList

urlpatterns = [
    path('', index_leaflet),
    path('2gis', index_gis),
    path(r'api/vehicles/', VehicleList.as_view(), name="vehicle_list")
]
