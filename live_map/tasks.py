import requests
import sqlite3
import os
from background_task import background
from krd_public_map.settings import BASE_DIR


def db_insert(data):
    print('db_insert')
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cur = conn.cursor()
    cur.execute('DELETE FROM live_map_vehicles')
    cur.executemany("""
        INSERT INTO
            live_map_vehicles (vehicle_type, route, lat, lng, speed, degree, vehicle_id)
        VALUES
            (:vehicle_type, :route, :lat, :lng, :speed, :degree, :vehicle_id)""", data)
    conn.commit()


@background
def get_gps_data():
    print("get_gps_data")
    r = requests.get('http://marsruty.ru/krasnodar/gps.txt')
    r.encoding = 'utf-8'
    raw_gps_data = r.text
    transport_data = []
    vehicle_types = {"1": "trolley", "2": "bus", "3": "tram"}
    for line in raw_gps_data.strip().split('\n'):
        vehicle_type, route, lng, lat, speed, degree, vehicle_id, *other = line.split(',')
        if vehicle_type in ('1', '2', '3') and route.startswith(tuple('0123456789')):
            transport_data.append({"vehicle_type": vehicle_types.get(vehicle_type),
                                   "route": str(route) if route else 0,
                                   "lat": float(lat[:2] + '.' + lat[2:]),
                                   "lng": float(lng[:2] + '.' + lng[2:]),
                                   "speed": int(speed) if speed else 0,
                                   "degree": int(degree) if degree else 0,
                                   "vehicle_id": vehicle_id})
    db_insert(transport_data)
    return transport_data
