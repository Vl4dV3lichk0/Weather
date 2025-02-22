from googletrans import  Translator
from autocorrect import Speller
import requests
import asyncio
import logging

# Translate your city in English
async def translate_text(text = ""):
  async with Translator() as translator:
    spell = Speller(lang="ru")
    text = spell(text)
    result = await translator.translate(text, dest="en")
    return result.text

class Weather:
    def __init__(self):
        # initialization

        # logger initialization
        logging.basicConfig(level=logging.INFO, filename="..\\logs\\log.log", filemode="w")

        # conditions initialization
        # coordinates
        self.lon = None
        self.lat = None
        # weather
        self.conditions = None
        self.description = None
        # main
        self.temp = None
        self.feels_like = None
        self.temp_min = None
        self.temp_max = None
        self.pressure = None
        self.humidity = None
        self.sea_level = None
        self.grnd_level = None
        # visibility
        self.visibility = None
        # wind
        self.wind_speed = None
        self.wind_deg = None
        self.wind_gust = None
        # sun
        self.sunrise = None
        self.sunset = None
        self.summary = None

        # city typing
        self.s_city = input("Введите название города: ")
        self.s_city = asyncio.run(translate_text(self.s_city))

        # for russian cities only
        #self.s_city += " , RU"

        # other signatures
        self.city_id = 0
        self.appid = "f77c13865d11b2918ed2c4ef8f33caf8"

        try:
            self.res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': self.s_city, 'type': 'like', 'units': 'metric', 'APPID': self.appid})
            self.data = self.res.json()
            self.cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in self.data['list']]
            self.city_id = self.data['list'][0]['id']
            logging.info("Initialization is successful")
        except Exception as e:
            logging.error(f"Exception (init): {e}")
            pass
        finally:
            self.gather()

    def gather(self):
        # getting weather conditions
        try:
            self.res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                    params={'id': self.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': self.appid})
            self.data = self.res.json()

            self.summary = self.get_coords, self.get_weather, self.get_main, self.get_visibility, self.get_wind, self.get_sun
            for function in self.summary:
                function()

            logging.info("Gathering is successful")
        except Exception as e:
            logging.warning(f"Exception (get): {e}")
            pass

    def get_coords(self):
        # coordinates
        try:
            self.lon = self.data['coord']['lon']
        except Exception as e:
            logging.warning(f"Exception (get_coords_lon): {e}")
            pass
        try:
            self.lon = self.data['coord']['lat']
        except Exception as e:
            logging.warning(f"Exception (get_coords_lat): {e}")
            pass

    def get_weather(self):
        # weather
        try:
            self.conditions = self.data['weather'][0]['main']
        except Exception as e:
            logging.warning(f"Exception (get_weather_main): {e}")
            pass
        try:
            self.description = self.data['weather'][0]['description']
        except Exception as e:
            logging.warning(f"Exception (get_weather_description): {e}")
            pass

    def get_main(self):
        # main
        try:
            self.temp = self.data['main']['temp']
        except Exception as e:
            logging.warning(f"Exception (get_main_temp): {e}")
            pass
        try:
            self.feels_like = self.data['main']['feels_like']
        except Exception as e:
            logging.warning(f"Exception (get_main_feels_like): {e}")
            pass
        try:
            self.temp_min = self.data['main']['temp_min']
        except Exception as e:
            logging.warning(f"Exception (get_main_temp_min): {e}")
            pass
        try:
            self.temp_max = self.data['main']['temp_max']
        except Exception as e:
            logging.warning(f"Exception (get_main_temp_max): {e}")
            pass
        try:
            self.pressure = self.data['main']['pressure']
        except Exception as e:
            logging.warning(f"Exception (get_main_pressure): {e}")
            pass
        try:
            self.humidity = self.data['main']['humidity']
        except Exception as e:
            logging.warning(f"Exception (get_main_humidity): {e}")
            pass
        try:
            self.sea_level = self.data['main']['sea_level']
        except Exception as e:
            logging.warning(f"Exception (get_main_sea_level): {e}")
            pass
        try:
            self.grnd_level = self.data['main']['grnd_level']
        except Exception as e:
            logging.warning(f"Exception (get_main_grnd_level): {e}")
            pass

    def get_visibility(self):
        # visibility
        try:
            self.grnd_level = self.data['visibility']
        except Exception as e:
            logging.warning(f"Exception (get_visibility): {e}")
            pass

    def get_wind(self):
        # wind
        try:
            self.wind_speed = self.data['wind']['speed']
        except Exception as e:
            logging.warning(f"Exception (get_wind_speed): {e}")
            pass
        try:
            self.wind_deg = self.data['wind']['deg']
        except Exception as e:
            logging.warning(f"Exception (get_wind_deg): {e}")
            pass
        try:
            self.wind_gust = self.data['wind']['gust']
        except Exception as e:
            logging.warning(f"Exception (get_wind_gust): {e}")
            pass

    def get_sun(self):
        # sun
        try:
            self.sunrise = self.data['sys']['sunrise']
        except Exception as e:
            logging.warning(f"Exception (get_sys_sunrise): {e}")
            pass
        try:
            self.sunset = self.data['sys']['sunset']
        except Exception as e:
            logging.warning(f"Exception (get_sys_sunset): {e}")
            pass

    def show_short(self):
        try:
            print("погода:", self.description)
            print("температура:", int(self.temp))
            print("ощущается как:", int(self.feels_like))
            print("Ветер (м/с):", int(self.wind_speed))
            print("Ветер (напр. в град.):", int(self.wind_deg))
            logging.info("Showing is successful")
        except Exception as e:
            logging.error(f"Exception (show_short): {e}")
            pass