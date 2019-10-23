from collections import defaultdict, OrderedDict
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VehicleSerializer
from live_map.models import Vehicles


class VehicleList(APIView):
    """
    # @@@ swag, later
    usage:
        krdmap.ddns.com/api/vehicles?fields={required_params}
        required_params list: bus,tram,trolley

    example:
        krdmap.ddns.com/api/vehicles?fields=bus,tram,trolley
        krdmap.ddns.com/api/vehicles?fields=bus,tram,trolley&with_keys=true
    result:
        returns JSON of specific Vehicles
    """

    def get(self, request):
        # allowed only "?fields=" params
        # that we will compare with 'request_params' after
        allowed_only_params = ["bus", "tram", "trolley"]

        # are there any "?fields=" params in 'request'
        if not request.query_params.get("fields"):
            return Response({"Error": {"required params": "bus,tram,trolley"}})

        # check if 'request' function parameters is acceptable
        # by comparing params from request with 'allowed_only_params' [line 27]
        params_raw = request.query_params.get("fields")
        params_prepared = params_raw.replace(" ", "").split(",")
        if not all(x in allowed_only_params for x in params_prepared):
            return Response({"Error": "check your params"})

        # @@@ later
        # returns {keys: values} pair instead of default {value} 
        with_keys_flag = request.query_params.get("with_keys", "false")

        # querying data from database and filter it
        # by excluding essential vehicles_type 
        # i.e. SQL: SELECT * FROM vehicles WHERE vehicle_type = {request params}
        queryset = Vehicles.objects.all().values()
        queryset = queryset.filter(vehicle_type__in=params_prepared)
        data = VehicleSerializer(queryset, many=True).data

        # @@@
        # at first loop we create unique [vehicle_type] keys from our database query
        vehicle_types = {key["vehicle_type"]: {} for key in data}
        response_dict = defaultdict(list, **vehicle_types)

        # and now we are going to fillup the dict that we will return later
        # and group keys() such as {vehicle_type} and {routes}
        # question: what's the point? answer: better view, less dict size
        if with_keys_flag == "true":
            for vehicle in data:
                if vehicle["route"] in response_dict[vehicle['vehicle_type']].keys():
                    response_dict[vehicle["vehicle_type"]][vehicle["route"]].append({
                        "vehicle_id": vehicle["vehicle_id"],
                        "lat": vehicle["lat"],
                        "lng": vehicle["lng"],
                        "speed": vehicle["speed"],
                        "degree": vehicle["degree"]})
                else:
                    response_dict[vehicle["vehicle_type"]][vehicle["route"]] = [{
                        "vehicle_id": vehicle["vehicle_id"],
                        "lat": vehicle["lat"],
                        "lng": vehicle["lng"],
                        "speed": vehicle["speed"],
                        "degree": vehicle["degree"]}]
        else:
            for vehicle in data:
                if vehicle["route"] in response_dict[vehicle['vehicle_type']].keys():
                    response_dict[vehicle["vehicle_type"]][vehicle["route"]].append([
                        vehicle["vehicle_id"],
                        vehicle["lat"],
                        vehicle["lng"],
                        vehicle["speed"],
                        vehicle["degree"]])
                else:
                    response_dict[vehicle["vehicle_type"]][vehicle["route"]] = [[
                        vehicle["vehicle_id"],
                        vehicle["lat"],
                        vehicle["lng"],
                        vehicle["speed"],
                        vehicle["degree"]]]

        return Response(response_dict)
