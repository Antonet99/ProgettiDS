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
from weather import get_weather_data, print_weather_data
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
        
        temp=round(weather_data['current']['temp'])
        pressure=round(weather_data['current']['pressure'])
        humidity=round(weather_data['current']['humidity'])
        wind=round(weather_data['current']['wind_speed'])
        wind_deg=round(weather_data['current']['wind_deg'])
        cond=(weather_data['current']['weather'][0]["description"])
        
        
        
        
        #print(response["temp"])
        #dispatcher.utter_message(text=print_weather_data(weather_data))

        return []