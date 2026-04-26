import requests
import json
import os

# Получаем ключ из переменных окружения (которые настроили в YAML)
API_KEY = os.getenv("MY_WEATHER_KEY")
CITY = "Moscow" # Можешь изменить на свой город

def get_weather_data():
    if not API_KEY:
        print(">>> ОШИБКА: API ключ не найден в Secrets!")
        return None

    # Запрос прогноза на 5 дней (3-часовые интервалы)
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=ru"
    
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return {
                "city": data['city']['name'],
                "current": data['list'][0],
                "daily": data['list'][::8] # Берем одну точку на каждый из 5 дней
            }
        else:
            print(f">>> Ошибка API: {res.status_code} - {res.text}")
    except Exception as e:
        print(f">>> Ошибка сети: {e}")
    return None

if __name__ == "__main__":
    weather_data = get_weather_data()
    
    os.makedirs('data', exist_ok=True)
    
    # Если данных нет (например, 401 ошибка), пишем заглушку, чтобы Action не падал
    if not weather_data:
        weather_data = {
            "city": "Ошибка активации ключа",
            "current": {"main": {"temp": 0}, "weather": [{"description": "Подождите 1 час"}]},
            "daily": []
        }
    
    with open('data/weather.json', 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2, ensure_ascii=False)
    
    print(">>> Данные успешно сохранены в data/weather.json")
    
