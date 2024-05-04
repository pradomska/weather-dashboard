#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Zadanie 4
Napisz program, który wygeneruje plik html z danymi pogodowymi dla wybranego przez Ciebie miasta.
Pobierz dowolny obrazek związany z pogodą z internetu i zapisz go w folderze z plikiem html.
Stwórz szablon html, który po uzupełnieniu danymi pogodowymi wyświetli obrazek oraz dane pogodowe.
Dane pogodowe uzyskasz z API: https://danepubliczne.imgw.pl/api/data/synop
"""

from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode
from urllib.parse import urljoin
import numpy as np
import requests
import pprint

BASE_URL = "https://danepubliczne.imgw.pl/api/data/synop/"


def get_weather_data():
    response = requests.get(BASE_URL)
    return response.json()


def get_unique_weather_station(weather_data):
    weather_station = [i["stacja"].upper() for i in weather_data]
    unique_station_names = np.unique(weather_station)
    return list(unique_station_names)


def input_name_station(station_names_list):
    while True:
        pprint.pp(station_names_list)
        station_name = input('Wybierz stację z wymienionych: ')
        if station_name.upper() in station_names_list:
            return station_name


def get_chosen_station_data(station_name):
    station_name = unidecode(station_name)
    response = requests.get(urljoin(BASE_URL, f'station/{station_name}'))
    return response.json()


def generate_html_template(station_response):
    file_loader = FileSystemLoader('./weather_template')
    env = Environment(loader=file_loader)
    template = env.get_template('template.html')

    rendered_template = template.render(stacja=station_response['stacja'],
                                        data_pomiaru=station_response["data_pomiaru"],
                                        godzina_pomiaru=station_response["godzina_pomiaru"],
                                        temperatura=station_response["temperatura"],
                                        predkosc_wiatru=station_response["predkosc_wiatru"],
                                        kierunek_wiatru=station_response["kierunek_wiatru"],
                                        wilgotnosc_wzgledna=station_response["wilgotnosc_wzgledna"],
                                        suma_opadu=station_response["suma_opadu"],
                                        cisnienie=station_response["cisnienie"]
                                        )

    with open("weather_template/output.html", "w", encoding='utf-8') as f:
        f.write(rendered_template)


def main():
    weather_data = get_weather_data()
    station_names = get_unique_weather_station(weather_data)
    chose_station = input_name_station(station_names)
    chosen_station_weather_data = get_chosen_station_data(chose_station)
    generate_html_template(chosen_station_weather_data)


if __name__ == "__main__":
    main()
