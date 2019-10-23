from django.apps import AppConfig


class LiveMapConfig(AppConfig):
    name = 'live_map'
    def ready(self):
        from .tasks import get_gps_data
        get_gps_data(repeat=5)
