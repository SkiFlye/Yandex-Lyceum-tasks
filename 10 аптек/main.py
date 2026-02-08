import sys
from pharmacy_search import find_pharmacies, get_coordinates, show_multiple_pharmacies


def main():
    if len(sys.argv) < 2:
        return
    address = " ".join(sys.argv[1:])
    toponym = get_coordinates(address)
    if not toponym:
        print("Адрес не найден")
        return
    toponym_coordinates = toponym["Point"]["pos"]
    longitude, latitude = map(float, toponym_coordinates.split())
    address_text = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    pharmacies = find_pharmacies(longitude, latitude, 10)
    if not pharmacies:
        print("Аптеки не найдены")
        return
    show_multiple_pharmacies((longitude, latitude), pharmacies)
    print(f"Исходный адрес: {address_text}")
    print(f"Найдено аптек: {len(pharmacies)}")
    for i, pharmacy in enumerate(pharmacies, 1):
        print(f"{i}.{pharmacy['name']}")
        print(f"Адрес: {pharmacy['address']}")
        print(f"Время работы: {pharmacy['hours'] or 'Нет данных'}")


if __name__ == "__main__":
    main()