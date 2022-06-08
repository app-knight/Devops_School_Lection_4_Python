import json
import time
import os
import cryptocode
import requests


# Read and write config
def config_handler(operation, config=''):
    with open('config.json', operation) as config_file:
        if operation == 'r':
            return json.load(config_file)
        elif operation == 'w':
            json.dump(config, config_file, indent = 4)


# Requesting data from api with simple retry mechanism
def get_data_from_api(request_url, request_timeout = 0, request_multiplier = 1):
    try:
         response = requests.get(request_url)
         if response.status_code != 200 :
             raise Exception('Request status incorrect') 
         response = json.loads(response.text)
    except Exception as e:
        if request_multiplier <= 5:
            # Increment time between queries
            time.wait(request_multiplier*request_timeout)
            response = get_data_from_api(request_url, request_timeout, request_multiplier)
        else:
            print(e)
            os._exit(0)
    return response


# Retrieve coordinates from API
def get_coordinates(config, api_key):
    if not 'coordinates' in config:
        request_url = config['geo_api_url'].format(config['city_name'], 1, api_key)
        response = get_data_from_api(request_url, config['request_timeout'])
        config['coordinates'] = (response[0]['lat'], response[0]['lon'])
        config_handler('w', config)
    return config


# Avoid users from storing plain API keys in configs, not ideal, but better then nothing
def hide_api_key(config):
    if 'api_key' in config:
        enc_api_key = cryptocode.encrypt(config['api_key'], config['passphrase'])
        config.pop('api_key')
        config['enc_api_key'] = enc_api_key
        config_handler('w', config)
    return config



if __name__ == "__main__":
    # Read config
    config = config_handler('r')
    # Hiding API key, if presented plain in config
    config = hide_api_key(config)
    # Decrypt API key
    api_key = cryptocode.decrypt(config['enc_api_key'], config['passphrase'])
    # Requesting coordinates for city. They are immutable, save them to config and save a looot of API calls
    config = get_coordinates(config, api_key)
    # Build weather request link
    weather_request_url = config['weather_api_url'].format(config['coordinates'][0], config['coordinates'][1], api_key, config['units'])
    # Getting weather data
    weather_data = get_data_from_api(weather_request_url, config['request_timeout'])
    # And display it finally
    print('Current weather in {0} - {1} - {2}. Temperature {3} °C, feels like {4} °C, pressure {5} hPa, humidity {6} %'.format(config['city_name'], weather_data['weather'][0]['main'], weather_data['weather'][0]['description'], weather_data['main']['temp'], weather_data['main']['feels_like'], weather_data['main']['pressure'], weather_data['main']['humidity']))