import requests
from core import error_handler
from config import OPENWEATHER_API_KEY

@error_handler.handle_errors
def get_weather_advice(city="Tokyo"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    response = requests.get(url).json()

    weather = response['weather'][0]['description']
    temp = response['main']['temp']

    advice = f"現在の{city}の天気は「{weather}」で、気温は{temp}度です。"
    if temp < 10:
        advice += "暖かい服装がおすすめです！🧥"
    elif "雨" in weather:
        advice += "傘を持っていった方がいいかも！🌂"
    else:
        advice += "過ごしやすい天気ですね！😊"

    return advice
