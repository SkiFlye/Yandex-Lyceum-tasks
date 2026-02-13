import os
import sys
import requests
import arcade
import math
from arcade.gui import UIManager, UIInputText, UITextArea, UIFlatButton, UIBoxLayout, UIDropdown

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Карта"
MAP_FILE = "map.png"
API_KEY = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
GEOCODER_API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'
SERVER_ADDRESS = 'https://static-maps.yandex.ru/1.x/'


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.lon = 133.7751
        self.lat = -25.2744
        self.marker_lon = self.lon
        self.marker_lat = self.lat
        self.zoom = 5
        self.zoom_step = 1
        self.zoom_min = 1
        self.zoom_max = 20
        self.lon_min = -180
        self.lon_max = 180
        self.lat_min = -90
        self.lat_max = 90
        self.background = None
        self.dark_theme = False
        self.object_address = ""
        self.object_address_without_index = ""
        self.object_postal_code = ""
        self.selected_option = "Выключить индекс"
        self.manager = UIManager()
        self.manager.enable()
        self.box_layout = UIBoxLayout(x=100, y=650, vertical=False, space_between=10)
        self.input_text = UIInputText(
            width=200, height=30,
            text_color=(255, 255, 255, 255),
            font_size=14)
        self.box_layout.add(self.input_text)
        self.reset_button = UIFlatButton(
            text="Сброс",
            width=100,
            height=30,
            color=arcade.color.DARK_RED)
        self.reset_button.on_click = self.on_reset_click
        self.box_layout.add(self.reset_button)
        self.postal_dropdown = UIDropdown(
            options=["Выключить индекс", "Включить индекс"],
            width=150,
            height=30)
        self.postal_dropdown.on_change = self.on_postal_change
        self.postal_dropdown.selected = "Выключить индекс"
        self.box_layout.add(self.postal_dropdown)
        self.manager.add(self.box_layout)
        self.setup()

    def on_postal_change(self, value):
        self.selected_option = value.new_value
        self.update_address_display()

    def update_address_display(self):
        if self.object_address_without_index:
            if self.selected_option == "Включить индекс" and self.object_postal_code:
                self.object_address = f"{self.object_address_without_index}, {self.object_postal_code}"
            else:
                self.object_address = self.object_address_without_index
        else:
            self.object_address = ""

    def on_reset_click(self, event):
        self.marker_lon = None
        self.marker_lat = None
        self.input_text.text = ""
        self.object_address = ""
        self.object_address_without_index = ""
        self.object_postal_code = ""
        self.selected_option = "Выключить индекс"
        self.postal_dropdown.selected = "Выключить индекс"
        self.update_map()

    def setup(self):
        self.get_image()

    def get_image(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.zoom,
            "l": "map",
            "apikey": API_KEY}
        if self.marker_lon is not None and self.marker_lat is not None:
            params["pt"] = f"{self.marker_lon},{self.marker_lat},pm2rdl"
        if self.dark_theme:
            params["theme"] = "dark"
        response = requests.get(SERVER_ADDRESS, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)
        self.background = arcade.load_texture(MAP_FILE)

    def update_map(self):
        self.get_image()

    def toggle_dark_theme(self):
        self.dark_theme = not self.dark_theme
        self.update_map()

    def get_postal_code(self, toponym):
        try:
            if "metaDataProperty" in toponym and "GeocoderMetaData" in toponym["metaDataProperty"]:
                geocoder_meta = toponym["metaDataProperty"]["GeocoderMetaData"]
                if "Address" in geocoder_meta and "postal_code" in geocoder_meta["Address"]:
                    return geocoder_meta["Address"]["postal_code"]
            pos = toponym["Point"]["pos"]
            lon, lat = pos.split()
            postal_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={GEOCODER_API_KEY}&geocode={lon},{lat}&format=json&kind=house"
            response = requests.get(postal_request)
            if response:
                json_response = response.json()
                if json_response["response"]["GeoObjectCollection"]["featureMember"]:
                    obj = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    if "metaDataProperty" in obj and "GeocoderMetaData" in obj["metaDataProperty"]:
                        if "Address" in obj["metaDataProperty"]["GeocoderMetaData"]:
                            if "postal_code" in obj["metaDataProperty"]["GeocoderMetaData"]["Address"]:
                                return obj["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except:
            pass
        return ""

    def search_object(self):
        search_text = self.input_text.text.strip()
        if not search_text:
            return
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={GEOCODER_API_KEY}&geocode={search_text}&format=json"
        response = requests.get(geocoder_request)
        if not response:
            print("Ошибка при поиске объекта")
            return
        json_response = response.json()
        found_objects = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not found_objects:
            print("Объект не найден")
            return
        toponym = found_objects[0]["GeoObject"]
        pos = toponym["Point"]["pos"]
        self.lon, self.lat = map(float, pos.split())
        self.marker_lon, self.marker_lat = self.lon, self.lat
        self.object_address_without_index = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        self.object_postal_code = self.get_postal_code(toponym)
        self.update_address_display()
        self.update_map()

    def get_coordinates_from_click(self, x, y):
        if not self.background:
            return None, None
        map_width = self.background.width
        map_height = self.background.height
        offset_x = (self.width - map_width) // 2
        offset_y = (self.height - map_height) // 2
        if x < offset_x or x > offset_x + map_width or y < offset_y or y > offset_y + map_height:
            return None, None
        map_x = x - offset_x
        map_y = y - offset_y
        c = 256 * 2 ** (self.zoom)
        lon = self.lon + (map_x - map_width / 2) * 360 / c
        lat = self.lat + (map_y - map_height / 2) * 360 / c
        return lon, lat

    def search_by_coordinates(self, lon, lat, pixel_x, pixel_y):
        self.marker_lon, self.marker_lat = lon, lat
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={GEOCODER_API_KEY}&geocode={lon},{lat}&format=json"
        response = requests.get(geocoder_request)
        if not response:
            print("Ошибка при поиске объекта")
            return
        json_response = response.json()
        found_objects = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not found_objects:
            print("Объект не найден")
            return
        toponym = found_objects[0]["GeoObject"]
        self.object_address_without_index = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        self.object_postal_code = self.get_postal_code(toponym)
        self.input_text.text = self.object_address_without_index
        self.update_address_display()
        self.update_map()

    def search_organization_by_coordinates(self, lon, lat):
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        search_params = {
            "apikey": api_key,
            "text": "организация",
            "lang": "ru_RU",
            "ll": f"{lon},{lat}",
            "type": "biz",
            "results": 1
        }
        response = requests.get(search_api_server, params=search_params)
        if not response:
            return None
        json_response = response.json()
        if not json_response.get("features"):
            return None

        organization = json_response["features"][0]
        org_coords = organization["geometry"]["coordinates"]
        org_lon, org_lat = org_coords

        lat_mid = (lat + org_lat) / 2
        lat_km_per_degree = 111.0
        lon_km_per_degree = 111.0 * math.cos(math.radians(lat_mid))
        lat_diff_km = (org_lat - lat) * lat_km_per_degree
        lon_diff_km = (org_lon - lon) * lon_km_per_degree
        distance_m = math.sqrt(lat_diff_km ** 2 + lon_diff_km ** 2) * 1000

        if distance_m > 50:
            return None

        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        hours = organization["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "Время работы не указано")

        return {
            "name": org_name,
            "address": org_address,
            "hours": hours,
            "distance": distance_m,
            "coordinates": (org_lon, org_lat)
        }

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(
                    (self.width - self.background.width) // 2,
                    (self.height - self.background.height) // 2,
                    self.background.width,
                    self.background.height))
        arcade.draw_rect_filled(arcade.rect.XYWH(300, 620, 580, 30), arcade.color.GRAY)
        arcade.draw_rect_outline(arcade.rect.XYWH(300, 620, 580, 30), arcade.color.WHITE, 2)
        if self.object_address:
            arcade.draw_text(f"Адрес: {self.object_address}",
                             20, 615,
                             arcade.color.BLACK, 12,
                             anchor_x="left")
        else:
            arcade.draw_text("Адрес: не найден",
                             20, 615,
                             arcade.color.BLACK, 12,
                             anchor_x="left")
        self.manager.draw()
        arcade.draw_text("Tab - Сменить тему",
                         10, 30,
                         arcade.color.WHITE, 12,
                         anchor_x="left")
        arcade.draw_text("Стрелки - движение, PgUp/PgDn - масштаб",
                         self.width // 2, 10,
                         arcade.color.WHITE, 10,
                         anchor_x="center")
        arcade.draw_text("Enter - поиск",
                         10, 670,
                         arcade.color.WHITE, 12,
                         anchor_x="left")

    def on_key_press(self, key, modifiers):
        updated = False
        move_amount = 0.5 / (2 ** self.zoom)

        if key == arcade.key.TAB:
            self.toggle_dark_theme()
            updated = True
        elif key == arcade.key.ENTER:
            self.search_object()
            updated = True
        elif key == arcade.key.PAGEUP:
            if self.zoom < self.zoom_max:
                self.zoom += self.zoom_step
                updated = True
        elif key == arcade.key.PAGEDOWN:
            if self.zoom > self.zoom_min:
                self.zoom -= self.zoom_step
                updated = True
        elif key == arcade.key.UP:
            self.lat += move_amount
            updated = True
        elif key == arcade.key.DOWN:
            self.lat -= move_amount
            updated = True
        elif key == arcade.key.LEFT:
            self.lon -= move_amount
            updated = True
        elif key == arcade.key.RIGHT:
            self.lon += move_amount
            updated = True

        if updated:
            self.update_map()

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.on_mouse_press(x, y, button, modifiers)
        if button == arcade.MOUSE_BUTTON_LEFT:
            lon, lat = self.get_coordinates_from_click(x, y)
            if lon is not None and lat is not None:
                self.search_by_coordinates(lon, lat, x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            lon, lat = self.get_coordinates_from_click(x, y)
            if lon is not None and lat is not None:
                self.marker_lon = None
                self.marker_lat = None
                self.input_text.text = ""
                self.object_address = ""
                self.object_address_without_index = ""
                self.object_postal_code = ""
                org = self.search_organization_by_coordinates(lon, lat)
                if org:
                    print(f"Найдена организация: {org['name']}")
                    print(f"Адрес: {org['address']}")
                    print(f"Время работы: {org['hours']}")
                    print(f"Расстояние: {org['distance']:.1f} м")
                else:
                    print("Организация не найдена в радиусе 50 метров")
                self.update_map()


def main():
    gameview = GameView()
    arcade.run()
    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)


if __name__ == "__main__":
    main()