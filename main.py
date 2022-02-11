import csv
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from haversine import haversine
import folium
import argparse


DATA = ['./loc100.csv', './loc500.csv', './loc1000.csv', './loc2500.csv', './loc10000.csv']
FILENAME = 'my_map.html'


def parse(year, path):
    """
    find all films from file that were mad in the give year
    """
    mas = []
    with open(path, 'r', encoding='ISO-8859-1') as file:
        f = csv.reader(file)
        geolocator = Nominatim(user_agent="zararaza")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.001)
        for row in f:
            if row[0] != year:
                continue
            try:
                location = geolocator.geocode(row[2])
                x1, y1 = location.latitude, location.longitude
                mas.append(((x1, y1), row[1]))
            except:
                pass
    return mas


def nearest_farthest(x, y, mas):
    """
    sorts all films due to the distance to the given point
    """
    how_much = 10
    mas.sort(key=lambda t: haversine(t[0], (x, y)))
    return mas[:how_much], mas[how_much:]


def create_map(mas1, mas2, filename):
    """
    creates a map with two layers form two given massives
    """
    map = folium.Map()
    near = folium.FeatureGroup(name="nearest")
    other = folium.FeatureGroup(name="other")
    html = """<h4>{}</h4>"""
    for cor, name in mas1:
        iframe = folium.IFrame(html=html.format(name), width=100, height=50)
        near.add_child(folium.Marker(location=cor, popup=folium.Popup(iframe), icon=folium.Icon(color="red")))
    for cor, name in mas2:
        iframe = folium.IFrame(html=html.format(name), width=100, height=50)
        other.add_child(folium.Marker(location=cor, popup=folium.Popup(iframe), icon=folium.Icon(color="blue")))
    map.add_child(near)
    map.add_child(other)
    map.add_child(folium.LayerControl())
    map.save(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('year', help="year")
    parser.add_argument('x', help='x coordinate')
    parser.add_argument('y', help='y coordinate')
    parser.add_argument('path', help='path to the csv document')
    args = parser.parse_args()
    year, x, y, path = args.year, args.x, args.y, args.path
    if path in DATA:
        if not x.isnumeric() or not y.isnumeric():
            print('x and y should be integers')
        mas1, mas2 = nearest_farthest(int(x), int(y), parse(year, path))
        create_map(mas1, mas2, FILENAME)
    else:
        print("no such a database exists")
