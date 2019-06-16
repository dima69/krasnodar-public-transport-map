var myMap = document.getElementById("map");
api_url = "http://127.0.0.1:8000/api/vehicles";

DG.then(function () {
    myMap = DG.map('map', {
        center: [45.032894, 39.021949],
        zoom: 13,
        fullscreenControl: false,
        zoomControl: false,
        geoclicker: false,
        poi: true
    });
    DG.control.location({position: 'bottomright'}).addTo(myMap);
    DG.control.traffic().addTo(myMap);

    getGpsDataFromAPI();
});

function getGpsDataFromAPI() {
    $.ajax("/api/vehicles", {
        method: "get",
        timeout: 3000,
        success: function (data) {
            // gps_data = data;
            console.log('ajax call');
            putMarkersNew(myMap, data);
        },
        error: function (error_data) {
            console.log("error", error_data);
        }
    });
}

function putMarkers(map_id, gps_data) {
    for (let vehicle of gps_data) {
        DG.marker([vehicle["latitude"], vehicle["longitude"]]).addTo(map_id);
    }
}

function putMarkersNew(map_id, gps_data) {
    DG.then(function() {
        return DG.plugin('/static/live_map/js/leaflet-beautify-marker-icon.js');
    }).then(function () {
        let lazy = '*Описание, что и куда едет, следующая остановка*, но мне лень ;)';
        for (let vehicle of gps_data) {
            if (vehicle["vehicle_type"] === "Автобус") {
                let bus_options = {
                    isAlphaNumericIcon: true,
                    text: vehicle["route"],
                    iconShape: 'marker',
                    borderWidth: 1,
                    borderColor: '#3379bf',
                    borderStyle: 'solid',
                    textColor: '#4071bf',
                    //iconSize: [26, 26],
                };
                L.marker([vehicle["latitude"], vehicle["longitude"]], {
                    icon: L.BeautifyIcon.icon(bus_options),
                    riseOnHover: true
                })
                    .addTo(map_id)
                    .bindPopup(`${vehicle["vehicle_type"]} № ${vehicle["route"]}<br>Скорость:${vehicle["speed"]} км/ч<br>${lazy}`)
                    .bindLabel(`${vehicle["vehicle_type"]} № ${vehicle["route"]}`);
            } else if(vehicle["vehicle_type"] === "Трамвай") {
                let tram_options = {
                    isAlphaNumericIcon: true,
                    text: vehicle["route"],
                    iconShape: 'marker',
                    borderWidth: 1,
                    borderColor: '#ffffff',
                    borderStyle: 'solid',
                    textColor: '#ffffff',
                    backgroundColor: '#f00',
                    //iconSize: [26, 26]
                };
                L.marker([vehicle["latitude"], vehicle["longitude"]], {
                    icon: L.BeautifyIcon.icon(tram_options),
                    riseOnHover: true
                })
                    .addTo(map_id)
                    .bindPopup(`${vehicle["vehicle_type"]} № ${vehicle["route"]}<br>Скорость:${vehicle["speed"]} км/ч<br>${lazy}`)
                    .bindLabel(`${vehicle["vehicle_type"]} № ${vehicle["route"]}`);
            } else {
                let troll_options = {
                    isAlphaNumericIcon: true,
                    text: vehicle["route"],
                    iconShape: 'marker',
                    borderWidth: 1,
                    borderColor: '#ffffff',
                    borderStyle: 'solid',
                    textColor: '#ffffff',
                    backgroundColor: '#f9650d',
                    //iconSize: [26, 26]
                };
                L.marker([vehicle["latitude"], vehicle["longitude"]], {
                    icon: L.BeautifyIcon.icon(troll_options),
                    riseOnHover: true
                })
                    .addTo(map_id)
                    .bindPopup(`${vehicle["vehicle_type"]} № ${vehicle["route"]}<br>Скорость:${vehicle["speed"]} км/ч<br>${lazy}`)
                    .bindLabel(`${vehicle["vehicle_type"]} № ${vehicle["route"]}`);
            }
        }
    })
}

// $(document).ready(function(){
//     setInterval(getGpsDataFromAPI,6000);
// });