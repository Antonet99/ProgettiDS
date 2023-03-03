import requests
import json
import datetime
import sys

def get_lat_lon(city):
    
    url = ( 
        f"http://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=2&appid=74b04930d39039f068ed4796e9baf28a"
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
        f"lat={get_lat_lon(city)[0]}&lon={get_lat_lon(city)[1]}"
        f"&lang=en"
        f"&units=metric"
        f"&exclude=hourly,daily,minutely"
        f"&appid=74b04930d39039f068ed4796e9baf28a"
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

    weather_data = {
        "lat": data["lat"],
        "lon": data["lon"],
        "timezone": data["timezone"],
        "datetime": str(datetime.datetime.fromtimestamp(data["current"]["dt"])),
        "main": data["current"]["weather"][0]["main"],
        "description": data["current"]["weather"][0]["description"].title(),
        "temp": data["current"]["temp"],
        "feels_like": data["current"]["feels_like"],
        "pressure": data["current"]["pressure"],
        "humidity": data["current"]["humidity"],
        "wind_speed": data["current"]["wind_speed"],
        "wind_deg": data["current"]["wind_deg"],
        "unit": "metric",
        "lang": "en",
    }
    
    return weather_data

def print_weather_data(weather_data):
    
    print(f"Location: {weather_data['lat']}, {weather_data['lon']}")
    print(f"Timezone: {weather_data['timezone']}")
    print(f"Current Time: {weather_data['datetime']}")
    print(f"Weather: {weather_data['description']} ({weather_data['main']})")
    print(f"Temperature: {weather_data['temp']}°C")
    print(f"Feels Like: {weather_data['feels_like']}°C")
    print(f"Pressure: {weather_data['pressure']} hPa")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")
    print(f"Wind Direction: {weather_data['wind_deg']}°")
    
def print_weather_data2(weather_data):
    return {
        "Latitude": weather_data["lat"],
        "Longitude": weather_data["lon"],
        "Timezone": weather_data["timezone"],
        "Datetime": weather_data["datetime"],
        "Weather Main": weather_data["main"],
        "Weather Description": weather_data["description"],
        "Temperature": f"{weather_data['temp']} °C",
        "Feels Like": f"{weather_data['feels_like']} °C",
        "Pressure": f"{weather_data['pressure']} hPa",
        "Humidity": f"{weather_data['humidity']} %",
        "Wind Speed": f"{weather_data['wind_speed']} m/s",
        "Wind Direction": f"{weather_data['wind_deg']}°",
        "Unit": weather_data["unit"],
        "Language": weather_data["lang"]
    }
