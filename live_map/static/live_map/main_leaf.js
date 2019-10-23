var map = L.map('mapid', {
    center: [45.032894, 39.021949],
    zoom: 13,
});

OpenStreetMap_Mapnik_Layer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function getGpsDataVanilla() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/vehicles/?fields=bus,tram,trolley&format=json");
    xhr.send();
    xhr.onload = function () {
        if (xhr.status != 200) {
            console.log(`Error ${xhr.status}: ${xhr.statusText}`);
        } else {
            var jsonResponse = JSON.parse(xhr.responseText);
            drawMarkersOnMapNew(jsonResponse);
        }
    };
}

// @@@ veh_type, route_number, speed
function drawCustomIcon(vehicle_type, route_number) {
    // if (vehicle_type === "bus") {
    //     classVehicleType = "bus-icon";
    // } else if (vehicle_type === "tram") {
    //     classVehicleType = "tram-icon";
    // } else {
    //     classVehicleType = "trolley-icon";
    // }
    switch (vehicle_type) {
        case "bus":
            classVehicleType = "bus-icon";
            break;
        case "tram":
            classVehicleType = "tram-icon";
            break;
        case "trolley":
            classVehicleType = "trolley-icon";
            break;
        default:
            break;
    }
    return L.divIcon({
        className: "vehicle-" + classVehicleType
    });
}

var markerslayer = L.layerGroup();
var markers_coords = [];
function drawMarkersOnMapNew(vehicles) {
    for (let type of Object.keys(vehicles)) {
        for (let route in vehicles[type]) {
            for (let item in vehicles[type][route]) {
                let marker = L.marker([
                    vehicles[type][route][item][1],
                    vehicles[type][route][item][2]
                ], {icon: drawCustomIcon(type, route)})
                    .bindPopup(`${type}<br>route:${route}<br>speed:${vehicles[type][route][item][3]}`);
                marker.addTo(markerslayer);
            }
        }
    }
    // markers_coords.addTo(markerslayer);
    markerslayer.addTo(map);
}

getGpsDataVanilla();