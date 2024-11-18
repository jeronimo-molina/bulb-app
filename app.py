import requests
import math
import os

# Get the API key from OpenWeather and put here the environment variable
api_key = ('Your OpenWeather_API_KEY')

def calculate_wet_bulb(temp, humidity):
    """
    Calcula a temperatura de bulbo úmido.
    Fórmula simplificada baseada em dados meteorológicos.
    """
    try:
        part1 = temp * math.atan(0.151977 * math.sqrt(humidity + 8.313659))
        part2 = math.atan(temp + humidity)
        part3 = math.atan(humidity - 1.676331)
        part4 = 0.00391838 * math.pow(humidity, 1.5) * math.atan(0.023101 * humidity)
        wet_bulb = part1 + part2 - part3 + part4 - 4.686035
        return round(wet_bulb, 2)
    except Exception as e:
        raise ValueError(f"Erro no cálculo: {e}")

def get_weather_data(city):
    """
    Fetches the current temperature and humidity for a given city from the OpenWeatherMap API.
    Args:
        city (str): The name of the city for which to fetch the weather data.
    Returns:
        dict: A dictionary containing the temperature and humidity.
    Raises:
        Exception: If there is an issue with the API request or data processing.
    """
    try:
        request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=metric'
        data = requests.get(request_url).json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        return {"temperature": temp, "humidity": humidity}
    except Exception as e:
        raise Exception(f"Erro ao buscar dados meteorológicos: {e}")

def main():
    city = input("Enter the city name: ")
    if not city:
        print("City parameter is required")
        return

    try:
        weather_data = get_weather_data(city)
        temp = weather_data['temperature']
        humidity = weather_data['humidity']
        wet_bulb_temp = calculate_wet_bulb(temp, humidity)
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wet Bulb Temperature: {wet_bulb_temp}°C")

        if wet_bulb_temp >= 35:
            print("Warning: Heat stress is possible")
        elif wet_bulb_temp > 27 and wet_bulb_temp < 35:
            print("Warning: You need to take precautions")
        else:
            print("No heat stress")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

