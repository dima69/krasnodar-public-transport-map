var myMap = document.getElementById("map");

DG.then(function () {
    return DG.plugin('/static/live_map/js/leaflet.canvas-markers.js');
}).then(function () {
    var markers = DG.layerGroup();
    myMap = DG.map('map', {
        // renderer: DG.canvas(),
        center: [45.032894, 39.021949],
        zoom: 13,
        fullscreenControl: false,
        zoomControl: false,
        geoclicker: false,
        poi: false
    });

    function refreshMarkers() {
        let gps_set = DG.ajax('/apimin/?q=bus,tram,trolley&format=json', {
            type: 'get',
            success: function(data) {
                mydata = data;
                newPutMarkers(data);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    function getGpsDataFromAPI() {
        $.ajax("/api/?q=bus,tram,trolley&format=json", {
            method: "get",
            dataType: 'json',
            success: function (data) {
                //newPutMarkers(data);
            },
            error: function (error_data) {
                console.log("error", error_data);
            }
        });
    }

    function newPutMarkers(gps_data) {
        markers.removeFrom(myMap);
        markers.clearLayers();
        for (let veh_type of Object.keys(gps_data)) {
            for (let route_number in gps_data[veh_type]) {
                for (let vehicle_item in gps_data[veh_type][route_number]) {
                    DG.marker([gps_data[veh_type][route_number][vehicle_item][1], gps_data[veh_type][route_number][vehicle_item][2]]).addTo(markers);
                }
            }
        }
        markers.addTo(myMap);
    }

    $(document).ready(refreshMarkers);

});