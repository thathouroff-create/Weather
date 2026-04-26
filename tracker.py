import requests
import json
import os

print(">>> СТАРТ: Погодный радар")

# Используй этот ключ (он проверен)
API_KEY = "bd5e378503939dec9256323a75109223"
CITY = "Moscow"

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=ru"
    try:
        print(f">>> Запрос погоды для {CITY}...")
        res = requests.get(url, timeout=15)
        print(f">>> Статус ответа: {res.status_code}")
        
        if res.status_code == 200:
            data = res.json()
            return {
                "city": data['city']['name'],
                "current": data['list'][0],
                "daily": data['list'][::8]
            }
        else:
            print(f">>> Ошибка API: {res.text}")
    except Exception as e:
        print(f">>> Ошибка сети: {e}")
    return None

if __name__ == "__main__":
    weather_data = get_weather()
    
    # ВСЕГДА создаем папку и файл, чтобы Git не выдавал ошибку
    os.makedirs('data', exist_ok=True)
    
    # Если данных нет, создаем "пустышку"
    if not weather_data:
        weather_data = {
            "city": "Ошибка данных",
            "current": {"main": {"temp": 0}, "weather": [{"description": "нет связи с API"}]},
            "daily": []
        }
    
    with open('data/weather.json', 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2, ensure_ascii=False)
        
    print(">>> Файл data/weather.json успешно создан.")
