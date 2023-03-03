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
import requests, datetime
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
            #wx_type = tracker.get_slot['wx_type']
            #api_key = "74b04930d39039f068ed4796e9baf28a"
            
            weather_data = get_weather_data(city)
            
            current_weather = weather_data['current']
            
            lat = weather_data['lat']
            lon = weather_data['lon']
            timezone = weather_data['timezone']
            dt = str(datetime.datetime.fromtimestamp(current_weather['dt']))
            sunrise = str(datetime.datetime.fromtimestamp(current_weather['sunrise']))
            sunset = str(datetime.datetime.fromtimestamp(current_weather['sunset']))
            temp = current_weather['temp']
            feels_like = current_weather['feels_like']
            pressure = current_weather['pressure']
            humidity = current_weather['humidity']
            uvi = current_weather['uvi']
            wind_speed = current_weather['wind_speed']
            wind_deg = current_weather['wind_deg']
            weather_description = current_weather['weather'][0]['description']
            if 'rain' in current_weather:
                rain = current_weather['rain']['1h']
            else:
                rain = 0.0
            
            response = f"Current weather in {city} ({lat}, {lon}) at {dt}: {weather_description}\n" \
                    f"Temperature: {temp} °C (Feels like {feels_like} °C)\n" \
                    f"Humidity: {humidity} %\n" \
                    f"Pressure: {pressure} hPa\n" \
                    f"UV index: {uvi}\n" \
                    f"Wind: {wind_speed} m/s, {wind_deg}°\n" \
                    f"Rain (last hour): {rain} mm\n" \
                    f"Timezone: {timezone}"
            
            dispatcher.utter_message(response)

            return []
