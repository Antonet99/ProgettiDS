# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import datetime
from weather import get_weather_data
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World from my first action!")

        return []


class Weather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        wx_type = tracker.get_slot('wx_type')

        if wx_type is None:
            wx_type = "meteo"

        # chiamata API che ritorna JSON con info meteo
        weather_data = get_weather_data(city)

        # info in variabile current_weather
        current_weather = weather_data['current']

        lat = weather_data['lat']
        lon = weather_data['lon']
        timezone = weather_data['timezone']
        dt = str(datetime.datetime.fromtimestamp(current_weather['dt']))
        temp = current_weather['temp']
        percepita = current_weather['feels_like']
        pressione = current_weather['pressure']
        umidità = current_weather['humidity']
        uvi = current_weather['uvi']
        vento_velocità = current_weather['wind_speed']
        vento_dir = current_weather['wind_deg']
        descrizione_meteo = current_weather['weather'][0]['description']
        if 'rain' in current_weather:
            pioggia = current_weather['rain']['1h']
        else:
            pioggia = 0
        # if 'alerts' in weather_data:
            # sender = weather_data['alerts'][0]['sender_name']
            # event = weather_data['alerts'][0]['event']
            # alert_descript = weather_data['alerts'][0]['description']
        # else:
            # alerts = None

        response = f"Mi dispiace, qualcosa è andato storto. Riprova!"

        match wx_type.lower():

            # ritorna tutto il meteo
            case "meteo":

                if pioggia > 0:
                    response = f"Meteo attuale a {city} ({lat}, {lon}) il {dt}: {descrizione_meteo}\n" \
                        f"Temperatura: {temp} °C (Percepita {percepita} °C)\n" \
                        f"Umidità: {umidità} %\n" \
                        f"Pressione: {pressione} hPa\n" \
                        f"Indice UV: {uvi}\n" \
                        f"Vento: {vento_velocità} m/s, {vento_dir}°\n" \
                        f"Pioggia (ultim'ora): {pioggia} mm\n" \
                        f"Timezone: {timezone}"
                else:
                    response = f"Meteo attuale a {city} ({lat}, {lon}) il {dt}: {descrizione_meteo}\n" \
                        f"Temperatura: {temp} °C (Percepita {percepita} °C)\n" \
                        f"Umidità: {umidità} %\n" \
                        f"Pressione: {pressione} hPa\n" \
                        f"Indice UV: {uvi}\n" \
                        f"Vento: {vento_velocità} m/s, {vento_dir}°\n" \
                        f"Attualmente non sta piovendo \n" \
                        f"Timezone: {timezone}"
                    # f"Alerts:\n" \
                    # f" - sender: {sender}\n" \
                    # f" - event: {event}\n" \
                    # f" - description: {alert_descript}\n" \

            # ritorna il singolo parametro richiesto dall'utente
            case "vento":
                response = f"La velocità attuale del vento a {city} ({lat}, {lon}) il {dt} è di {vento_velocità} metri al secondo da {vento_dir} gradi. "

            case "temperatura":
                response = f"La temperatura attuale a {city} ({lat}, {lon}) il {dt} è {temp}°C. "

            case "pressione":
                response = f"La pressione attuale dell'aria a {city} ({lat}, {lon}) il {dt} è {pressione} hPa. "

            case "umidità":
                response = f"L'umidità attuale a {city} ({lat}, {lon}) il {dt} è {umidità}%. "

            case "uvi":
                response = f"L'indice UV attuale a {city} ({lat}, {lon}) il {dt} è {uvi}. "

            case "pioggia":
                if pioggia != 0:
                    response = f"La pioggia nell'ultima ora a {city} ({lat}, {lon}) il {dt} è stata di {pioggia} mm. "
                else:
                    response = f"Non sta piovendo in questo momento a {city} ({lat}, {lon}). "

        dispatcher.utter_message(response)

        return []
