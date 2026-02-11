import os
import sys
import requests
import arcade
from arcade.gui import UIManager, UIInputText, UITextArea

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
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
        self.zoom = 5
        self.zoom_step = 1
        self.move_step = 1
        self.zoom_min = 1
        self.zoom_max = 20
        self.lon_min = -180
        self.lon_max = 180
        self.lat_min = -90
        self.lat_max = 90
        self.background = None
        self.dark_theme = False
        self.manager = UIManager()
        self.manager.enable()
        self.input_text = UIInputText(
            x=100, y=550,
            width=400, height=30,
            text_color=(255, 255, 255, 255),
            font_size=14)
        self.manager.add(self.input_text)
        self.setup()

    def setup(self):
        self.get_image()

    def get_image(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.zoom,
            "l": "map",
            "apikey": API_KEY}
        params["pt"] = f"{self.lon},{self.lat},pm2rdl"
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
        self.update_map()

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
                         10, 570,
                         arcade.color.WHITE, 12,
                         anchor_x="left")

    def on_key_press(self, key, modifiers):
        updated = False
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
            if self.lat + self.move_step <= self.lat_max:
                self.lat += self.move_step
                updated = True
        elif key == arcade.key.DOWN:
            if self.lat - self.move_step >= self.lat_min:
                self.lat -= self.move_step
                updated = True
        elif key == arcade.key.LEFT:
            if self.lon - self.move_step >= self.lon_min:
                self.lon -= self.move_step
                updated = True
        elif key == arcade.key.RIGHT:
            if self.lon + self.move_step <= self.lon_max:
                self.lon += self.move_step
                updated = True
        if updated:
            self.update_map()

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.on_mouse_press(x, y, button, modifiers)


def main():
    gameview = GameView()
    arcade.run()
    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)


if __name__ == "__main__":
    main()