import requests
import random
import arcade
from map_utils import calculate_map_params

APIkey = '8013b162-6b42-4997-9691-77b7074026e0'
static_api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
MAP_FILE = "map.png"
CITIES = [
    "Москва",
    "Санкт-Петербург",
    "Казань",
    "Сочи",
    "Екатеринбург",
    "Новосибирск",
    "Владивосток",
    "Якутск",
    "Калининград"]


class CityGuessGame(arcade.Window):
    def __init__(self):
        super().__init__(700, 700, "Угадай город")
        self.cities = random.sample(CITIES, len(CITIES))
        self.current_slide = 0
        self.background = None
        self.current_city_name = ""
        self.show_city = False
        self.city_lon = 0
        self.city_lat = 0
        self.square_size = 150
        self.setup()

    def setup(self):
        self.get_image()

    def get_image(self):
        city = self.cities[self.current_slide]
        self.current_city_name = city
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={APIkey}&geocode={city}&format=json"
        response = requests.get(geocoder_request)
        if not response:
            return
        json_response = response.json()
        found_objects = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not found_objects:
            return
        toponym = found_objects[0]["GeoObject"]
        pos = toponym["Point"]["pos"]
        self.city_lon, self.city_lat = map(float, pos.split())
        map_params = calculate_map_params(toponym, padding_factor=0.5)
        ll = map_params["ll"]
        spn = map_params["spn"]
        pt_param = f"{self.city_lon},{self.city_lat},pm2rdl"
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={pt_param}&apikey={static_api_key}"
        response = requests.get(map_request)
        if response:
            with open(MAP_FILE, "wb") as file:
                file.write(response.content)
            self.background = arcade.load_texture(MAP_FILE)
        self.square_size = len(self.current_city_name) * 10

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.LBWH((self.width - self.background.width) // 2,
                                                 (self.height - self.background.height) // 2,
                                                 self.background.width, self.background.height))
            if not self.show_city:
                arcade.draw_rect_filled(arcade.rect.XYWH(self.width // 2, self.height // 2,
                                                         self.square_size, 30), arcade.color.BLACK)
        arcade.draw_text("Игра: Угадай город по карте",
                         self.width // 2, 670,
                         arcade.color.WHITE, 20,
                         anchor_x="center")
        arcade.draw_text("Пробел - показать/скрыть ответ",
                         20, 30,
                         arcade.color.LIGHT_GRAY, 16)
        arcade.draw_text("Enter - следующий слайд",
                         self.width - 20, 30,
                         arcade.color.LIGHT_GRAY, 16,
                         anchor_x="right")
        if self.show_city:
            arcade.draw_text(f"Ответ: {self.current_city_name}",
                             self.width // 2, 630,
                             arcade.color.GREEN, 24,
                             anchor_x="center")

    def next_slide(self):
        self.show_city = False
        self.current_slide = (self.current_slide + 1) % len(self.cities)
        self.get_image()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.show_city = not self.show_city
            self.get_image()
        if key == arcade.key.ENTER:
            self.next_slide()

    def on_mouse_press(self, x, y, button, modifiers):
        self.next_slide()


def main():
    game = CityGuessGame()
    arcade.run()


if __name__ == "__main__":
    main()