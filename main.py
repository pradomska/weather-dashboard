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
from pydantic import BaseModel
import numpy as np
import requests
import pprint

BASE_URL = "https://danepubliczne.imgw.pl/api/data/synop/"


class WeatherStationResponse(BaseModel):
    stacja: str
    data_pomiaru: str | None
    godzina_pomiaru: str | None
    temperatura: float
    predkosc_wiatru: float | None
    kierunek_wiatru: str | None
    wilgotnosc_wzgledna: float | None
    suma_opadu: float
    cisnienie: float


def get_weather_data_response():
    response = requests.get(BASE_URL)
    return response.json()


def get_unique_weather_station_names(weather_data_response):
    return list(np.unique([i["stacja"].upper() for i in weather_data_response]))


def input_name_station_by_user(station_names_list):
    while True:
        pprint.pp(station_names_list)
        station_name = input('Wybierz stację z wymienionych: ')
        if station_name.upper() in station_names_list:
            return station_name


def get_chosen_station_data(station_name, weather_data_response):
    station_name = f'{station_name.title()}'
    for element in weather_data_response:
        if element['stacja'] == station_name:
            print(WeatherStationResponse(**element))
            return WeatherStationResponse(**element)


def render_html_report(weather_station_response):
    file_loader = FileSystemLoader('./weather_template')
    env = Environment(loader=file_loader)
    template = env.get_template('template.html')

    rendered_template = template.render(stacja=weather_station_response.stacja,
                                        data_pomiaru=weather_station_response.data_pomiaru,
                                        godzina_pomiaru=weather_station_response.godzina_pomiaru,
                                        temperatura=weather_station_response.temperatura,
                                        predkosc_wiatru=weather_station_response.predkosc_wiatru,
                                        kierunek_wiatru=weather_station_response.kierunek_wiatru,
                                        wilgotnosc_wzgledna=weather_station_response.wilgotnosc_wzgledna,
                                        suma_opadu=weather_station_response.suma_opadu,
                                        cisnienie=weather_station_response.cisnienie
                                        )

    with open("weather_template/output.html", "w", encoding='utf-8') as f:
        f.write(rendered_template)


def main():
    weather_data_response = get_weather_data_response()
    station_names = get_unique_weather_station_names(weather_data_response)
    chose_station = input_name_station_by_user(station_names)
    chosen_station_weather_data = get_chosen_station_data(chose_station, weather_data_response)
    render_html_report(chosen_station_weather_data)


if __name__ == "__main__":
    main()
