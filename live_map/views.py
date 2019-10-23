from django.shortcuts import render


def index_gis(request):
    return render(request, "index_gis.html")


def index_leaflet(request):
      return render(request, "index_leaflet.html")
