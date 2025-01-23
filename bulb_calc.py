import os
import requests
import math

def calculate_wet_bulb(temp, humidity):
    """
    Calcula a temperatura de bulbo úmido usando uma fórmula simplificada baseada em dados meteorológicos.
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
    Obtém dados meteorológicos e a bandeira do país usando a API do OpenWeatherMap e countryflags.io.
    """
    try:
        # Obtenha os dados meteorológicos
        request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=metric'
        data = requests.get(request_url).json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        country_code = data['sys']['country']

        return {"temperature": temp, "humidity": humidity, "country": country_code}
    except Exception as e:
        raise Exception(f"Erro ao buscar dados meteorológicos: {e}")

def get_alert_message(wet_bulb_temp):
    """
    Generates an alert message based on the wet-bulb temperature.
    """
    if wet_bulb_temp > 35:
        return "Life risk! Seek an air-conditioned place immediately!"
    elif wet_bulb_temp >= 31:
        return "Danger! Seek an air-conditioned place. Risk of life for sensitive people."
    elif wet_bulb_temp >= 23:
        return "Alert! Look for a cool place."
    else:
        return "Normal temperature."

if __name__ == "__main__":
    city = input("Digite o nome da cidade: ")
    if not city:
        print("City parameter is required")
    else:
        try:
            weather_data = get_weather_data(city)
            temp = weather_data['temperature']
            humidity = weather_data['humidity']
            country = weather_data['country']
            flag = weather_data['flag']
            wet_bulb_temp = calculate_wet_bulb(temp, humidity)
            alert_message = get_alert_message(wet_bulb_temp)
            print(f"City: {city}, {country}")
            print(f"Temperature: {temp}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wet Bulb Temperature: {wet_bulb_temp}°C")
            print(f"Flag: {flag}")
            print(alert_message)
        except Exception as e:
            print(e)
