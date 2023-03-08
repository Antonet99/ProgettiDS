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
            wx_type = tracker.get_slot('wx_type')
            
            if wx_type is None:
                wx_type = "weather"
                
            #api_key = "74b04930d39039f068ed4796e9baf28a"
            
            # chiamata API che ritorna JSON con info meteo
            weather_data = get_weather_data(city)
            
            # info in variabile current_weather
            current_weather = weather_data['current']
            
            lat = weather_data['lat']
            lon = weather_data['lon']
            timezone = weather_data['timezone']
            dt = str(datetime.datetime.fromtimestamp(current_weather['dt']))
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
                rain = 0
            if 'alerts' in weather_data:
                sender = weather_data['alerts'][0]['sender_name']
                event = weather_data['alerts'][0]['event']
                alert_descript = weather_data['alerts'][0]['description']
            else:
                alerts = None
                
            response = f"I'm sorry, something went bad. Try again!"
            
            match wx_type.lower():
                
                # ritorna tutto il meteo
                case "weather":
                    
                    if rain > 0:
                        response = f"Current weather in {city} ({lat}, {lon}) at {dt}: {weather_description}\n" \
                                    f"Temperature: {temp} °C (Feels like {feels_like} °C)\n" \
                                    f"Humidity: {humidity} %\n" \
                                    f"Pressure: {pressure} hPa\n" \
                                    f"UV index: {uvi}\n" \
                                    f"Wind: {wind_speed} m/s, {wind_deg}°\n" \
                                    f"Rain (last hour): {rain} mm\n" \
                                    f"Timezone: {timezone}"
                    else:
                        response = f"Current weather in {city} ({lat}, {lon}) at {dt}: {weather_description}\n" \
                                    f"Temperature: {temp} °C (Feels like {feels_like} °C)\n" \
                                    f"Humidity: {humidity} %\n" \
                                    f"Pressure: {pressure} hPa\n" \
                                    f"UV index: {uvi}\n" \
                                    f"Wind: {wind_speed} m/s, {wind_deg}°\n" \
                                    f"Rain: It's not raining right now\n" \
                                    f"Timezone: {timezone}\n"
                                    #f"Alerts:\n" \
                                    #f" - sender: {sender}\n" \
                                    #f" - event: {event}\n" \
                                    #f" - description: {alert_descript}\n" \
                 
                # ritorna il singolo parametro richiesto dall'utente
                case "wind":
                    response = f"The current wind speed in {city} ({lat}, {lon}) at {dt} is {wind_speed} metres per second from {wind_deg} degrees. "
                
                case "temperature":
                    response = f"The current temperature in {city} ({lat}, {lon}) at {dt} is {temp}°C. "
                
                case "pressure":
                    response = f"The current air pressure in {city} ({lat}, {lon}) at {dt} is {pressure} hPa. "
                
                case "humidity":
                    response = f"The current humidity in {city} ({lat}, {lon}) at {dt} is {humidity}%. "
                
                case "uvi":
                    response = f"The current UV index in {city} ({lat}, {lon}) at {dt} is {uvi}. "
                
                case "rain":      
                    if rain != 0:
                        response = f"The rain in the last hour in {city} ({lat}, {lon}) at {dt} is {rain} mm. "
                    else:
                        response=f"It's not raining right now in {city} ({lat}, {lon}). "

            dispatcher.utter_message(response)
                
            return []

