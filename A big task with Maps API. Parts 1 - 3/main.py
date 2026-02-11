import os
import sys
import requests
import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Карта"
MAP_FILE = "map.png"
API_KEY = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
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
        self.setup()

    def setup(self):
        self.get_image()

    def get_image(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.zoom,
            "l": "map",
            "apikey": API_KEY}
        response = requests.get(SERVER_ADDRESS, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
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
        arcade.draw_text("Стрелки - движение, PgUp/PgDn - масштаб",
                         self.width // 2, 10,
                         arcade.color.WHITE, 10,
                         anchor_x="center")

    def on_key_press(self, key, modifiers):
        updated = False
        if key == arcade.key.PAGEUP:
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


def main():
    gameview = GameView()
    arcade.run()
    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)


if __name__ == "__main__":
    main()