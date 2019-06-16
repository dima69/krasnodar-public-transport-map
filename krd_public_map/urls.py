from django.urls import path, include


urlpatterns = [
    path('', include('live_map.urls'))
]

