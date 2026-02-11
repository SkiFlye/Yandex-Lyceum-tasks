import os
import sys
import requests
import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Карта"
MAP_FILE = "map.png"
API_KEY = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
SERVER_ADDRESS = 'https://static-maps.yandex.ru/v1?'


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.lon = 133.7751
        self.lat = -25.2744
        self.zoom = 55
        self.zoom_step = 5
        self.move_step = 1.0
        self.zoom_min = 1
        self.zoom_max = 90
        self.lon_min = -180
        self.lon_max = 180
        self.lat_min = -90
        self.lat_max = 90
        self.background = None
        self.setup()

    def setup(self):
        self.get_image()

    def get_image(self):
        ll_spn = f'll={self.lon},{self.lat}&spn={self.zoom},{self.zoom}'
        map_request = f"{SERVER_ADDRESS}{ll_spn}&apikey={API_KEY}"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)
        self.background = arcade.load_texture(MAP_FILE)

    def update_map(self):
        self.get_image()

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

    def on_key_press(self, key, modifiers):
        updated = False
        if key == arcade.key.PAGEUP:
            new_zoom = self.zoom - self.zoom_step
            if new_zoom >= self.zoom_min:
                self.zoom = new_zoom
                updated = True
        elif key == arcade.key.PAGEDOWN:
            new_zoom = self.zoom + self.zoom_step
            if new_zoom < self.zoom_max:
                self.zoom = new_zoom
                updated = True
        elif key == arcade.key.UP:
            new_lat = self.lat + self.move_step
            if new_lat < self.lat_max:
                self.lat = new_lat
                updated = True
        elif key == arcade.key.DOWN:
            new_lat = self.lat - self.move_step
            if new_lat >= self.lat_min:
                self.lat = new_lat
                updated = True
        elif key == arcade.key.LEFT:
            new_lon = self.lon - self.move_step
            if new_lon >= self.lon_min:
                self.lon = new_lon
                updated = True
        elif key == arcade.key.RIGHT:
            new_lon = self.lon + self.move_step
            if new_lon <= self.lon_max:
                self.lon = new_lon
                updated = True
        if updated:
            self.update_map()


def main():
    gameview = GameView()
    arcade.run()
    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)


if __name__ == "__main__":
    main()