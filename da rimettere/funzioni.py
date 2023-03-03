import requests
import json
import datetime
import sys

path = "/Users/antoniobaio/Desktop/Progetti/ProgettiDS/Chatbot_RASA/config.json"

def configuration():

    config = {}

    config["api_key"] = input("OWM API key: ")
    config["city"] = input("City: ")
    config["unit"] = input("Unit (metric/imperial) : ") or "metric"
    config["lang"] = input("Language: ") or "it"
    config["limit"] = input("Limit of response: ") or 2

    with open(path, "w+") as config_json:
        json.dump(config, config_json, indent=4)

    return "Configuration finished."

def get_config_data():
    
    config = {}

    with open("config.json") as config_json:
        data = json.load(config_json)
        config = {key: value for key, value in data.items()}

    return config

def get_lat_lon(city):
    
    #config = get_config_data()  
    #api_key = config["api_key"]  
    #city = config["city"]
    #limit = config["limit"]

    url = ( 
        f"http://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=2&appid={api_key}"
    )
    response = requests.get(url)
    
    if response.status_code == 200:
         # parsing della risposta JSON
        data = response.json()
        if len(data) > 0:
            # accesso alle coordinate geografiche della città
            lat = data[0]['lat']
            lon = data[0]['lon']
            
            lat = round(lat, 1)
            lon = round(lon, 1)
            
            return lat, lon
        else:
            print(f"Non sono state trovate informazioni geografiche per la città di {city}")
    else: 
        print("Errore durante la richiesta delle informazioni geografiche")


def get_weather_data(city):
    """Get weather data from the API and return the necessary data."""
    
    #config = get_config_data()  
    #city = config["city"]
    
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={get_lat_lon()[0]}&lon={get_lat_lon()[1]}"
        f"&lang={get_config_data()['lang']}"
        f"&units={get_config_data()['unit']}"
        f"&exclude=hourly,daily,minutely"
        f"&appid={get_config_data()['api_key']}"
    )
    
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
    except requests.HTTPError:
        status = response.status_code
        if status == 401:
            print("Invalid API key.")
        elif status == 404:
            print("Invalid input.")
        elif status in (429, 443):
            print("API calls per minute exceeded.")

        sys.exit(1)

    data = response.json()

    weather_info = {
        "lat": data["lat"],
        "lon": data["lon"],
        "timezone": data["timezone"],
        "main": data["current"]["weather"][0]["main"],
        "description": data["current"]["weather"][0]["description"].title(),
        "temp": data["current"]["temp"],
        "feels_like": data["current"]["feels_like"],
        "pressure": data["current"]["pressure"],
        "humidity": data["current"]["humidity"],
        "wind_speed": data["current"]["wind_speed"],
        "wind_deg": data["current"]["wind_deg"],
        "unit": get_config_data()['unit'],
        "lang": get_config_data()['lang'],
    }
    
    return weather_info

