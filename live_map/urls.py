from live_map import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'vehicles', views.VehicleView)

urlpatterns = [
    path('', views.index),
    path('api/', include(router.urls)),
    path(r'docs/', include_docs_urls(title='Public map API')),
]
