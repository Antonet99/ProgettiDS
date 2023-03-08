import requests
import json
import sys

def get_lat_lon(city):
    
    url = ( 
        f"http://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=2&appid=7f4eb755102bc64c01058478e0fcc91a"
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
        f"&appid=7f4eb755102bc64c01058478e0fcc91a"
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

    weather_data = response.json()

    return weather_data