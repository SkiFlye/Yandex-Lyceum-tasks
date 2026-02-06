import sys
from io import BytesIO
import requests
from PIL import Image
from map_utils import calculate_map_params


def search_address(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    found_objects = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if not found_objects:
        print("Объект не найден")
        return None
    toponym = found_objects[0]["GeoObject"]
    toponym_coordinates = toponym["Point"]["pos"]
    longitude, latitude = toponym_coordinates.split()
    map_params = calculate_map_params(toponym)
    map_params.update({
        "l": "map",
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "pt": f"{longitude},{latitude},pm2rdl"})
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.show()
    print("Найден объект:", toponym["metaDataProperty"]["GeocoderMetaData"]["text"])
    print("Координаты:", f"{longitude}, {latitude}")
    return {
        "toponym": toponym,
        "coordinates": (float(longitude), float(latitude)),
        "map_params": map_params}

def main():
    address = " ".join(sys.argv[1:])
    search_address(address)

if __name__ == "__main__":
    main()