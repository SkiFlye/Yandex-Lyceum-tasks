import sys
from io import BytesIO
import requests
from PIL import Image
from map_utils import calculate_map_params
import math

def get_coordinates(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return None
    json_response = response.json()
    found_objects = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if not found_objects:
        return None
    toponym = found_objects[0]["GeoObject"]
    return toponym

def find_nearest_pharmacy(lon, lat):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": f"{lon},{lat}",
        "type": "biz",
        "results": 10}
    response = requests.get(search_api_server, params=search_params)
    if not response:
        return None
    json_response = response.json()
    if not json_response.get("features"):
        return None
    nearest = None
    min_distance = float('inf')
    for feature in json_response["features"]:
        point = feature["geometry"]["coordinates"]
        ph_lon, ph_lat = point
        lat_mid = (lat + ph_lat) / 2
        lat_km = 111.0
        lon_km = 111.0 * math.cos(math.radians(lat_mid))
        lat_diff = (ph_lat - lat) * lat_km
        lon_diff = (ph_lon - lon) * lon_km
        distance = math.sqrt(lat_diff**2 + lon_diff**2) * 1000
        if distance < min_distance:
            min_distance = distance
            nearest = {
                "coordinates": (ph_lon, ph_lat),
                "name": feature["properties"]["CompanyMetaData"]["name"],
                "address": feature["properties"]["CompanyMetaData"]["address"],
                "hours": feature["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "Время работы не указано"),
                "distance": distance}
    return nearest

def create_combined_toponym(point1, point2):
    lon1, lat1 = point1
    lon2, lat2 = point2
    min_lon = min(lon1, lon2)
    max_lon = max(lon1, lon2)
    min_lat = min(lat1, lat2)
    max_lat = max(lat1, lat2)
    virtual_toponym = {
        "Point": {"pos": f"{(lon1 + lon2) / 2} {(lat1 + lat2) / 2}"},
        "boundedBy": {
            "Envelope": {
                "lowerCorner": f"{min_lon} {min_lat}",
                "upperCorner": f"{max_lon} {max_lat}"}}}
    return virtual_toponym

def show_map(address_point, pharmacy_point):
    virtual_toponym = create_combined_toponym(address_point, pharmacy_point)
    map_params = calculate_map_params(virtual_toponym, padding_factor=2.0)
    address_marker = f"{address_point[0]},{address_point[1]},pm2rdl"
    pharmacy_marker = f"{pharmacy_point[0]},{pharmacy_point[1]},pm2gnm"
    map_params.update({
        "l": "map",
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "pt": f"{address_marker}~{pharmacy_marker}"})
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if response:
        im = BytesIO(response.content)
        Image.open(im).show()
    return response is not None

def print_result(address_text, address_coords, pharmacy):
    print("Исходный адрес:")
    print(f"{address_text}")
    print("Ближайшая аптека:")
    print(f"Название: {pharmacy['name']}")
    print(f"Адрес: {pharmacy['address']}")
    print(f"Время работы: {pharmacy['hours']}")
    print(f"Расстояние: {pharmacy['distance']:.0f} метров")

def main():
    address = " ".join(sys.argv[1:])
    toponym = get_coordinates(address)
    if not toponym:
        print("Адрес не найден")
        return
    toponym_coordinates = toponym["Point"]["pos"]
    longitude, latitude = map(float, toponym_coordinates.split())
    address_text = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    pharmacy = find_nearest_pharmacy(longitude, latitude)
    if not pharmacy:
        print("Аптеки не найдены")
        return
    show_map((longitude, latitude), pharmacy["coordinates"])
    print_result(address_text, (longitude, latitude), pharmacy)

if __name__ == "__main__":
    main()