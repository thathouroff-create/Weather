import requests
import json
import os

# Используй свой API Key от OpenWeatherMap
API_KEY = "604b73696fe82cfda93d7d8278c9faff" # Тестовый ключ
CITY = "Moscow" 

def get_weather_forecast():
    # Запрос прогноза на 5 дней с шагом 3 часа
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=ru"
    
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            
            # Формируем структуру для фронтенда
            forecast_data = {
                "city": data['city']['name'],
                "current": data['list'][0], # Ближайший прогноз
                "daily": data['list'][::8]   # Выборка раз в сутки (прогноз на 5 дней)
            }
            return forecast_data
    except Exception as e:
        print(f"Ошибка сбора данных: {e}")
    return None

if __name__ == "__main__":
    weather = get_weather_forecast()
    if weather:
        os.makedirs('data', exist_ok=True)
        with open('data/weather.json', 'w', encoding='utf-8') as f:
            json.dump(weather, f, indent=2, ensure_ascii=False)
        print("Данные погоды обновлены.")
      
