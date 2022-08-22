from datetime import datetime
import flag

# Globals
DESCRIPTION = ""
TEMP: float = 0.0
FEELS_LIKE: float = 0.0
TEMP_MIN: float = 0.0
TEMP_MAX: float = 0.0
PRESSURE = ""
HUMIDITY = ""
SEA_LEVEL = ""
VISIBILITY = ""
WIND_SPEED = ""
COUNTRY = ""
SUNRISE = ""
SUNSET = ""
TIMEZONE = ""

def get_weather_report(response: dict, is_arabic: bool) -> str:
    global DESCRIPTION, TEMP, FEELS_LIKE, TEMP_MIN, TEMP_MAX, PRESSURE, HUMIDITY, SEA_LEVEL, VISIBILITY, WIND_SPEED, COUNTRY, SUNRISE, SUNSET, TIMEZONE

    main = response['main']
    wind = response['wind']
    country_data = response['sys']
    sunrise = datetime.fromtimestamp(country_data['sunrise'])
    sunset = datetime.fromtimestamp(country_data['sunset'])

    DESCRIPTION = response['weather'][0]['description']
    TEMP = response['main']['temp']
    FEELS_LIKE = main['feels_like']
    TEMP_MIN = main['temp_min']
    TEMP_MAX = main['temp_max']
    PRESSURE = main['pressure']
    HUMIDITY = main['humidity']
    SEA_LEVEL = str(main.get('sea_level', ""))
    SEA_LEVEL = SEA_LEVEL + " mb" if SEA_LEVEL != "" else ""
    VISIBILITY = response['visibility']
    WIND_SPEED = wind['speed']
    COUNTRY = country_data['country']
    SUNRISE = datetime.fromtimestamp(country_data['sunrise']).time()
    SUNSET = datetime.fromtimestamp(country_data['sunset']).time()
    # TIMEZONE = response['timezone']

    REPORT = f"""\tWeather: {DESCRIPTION} 🛰️
Temperature: {TEMP:.2f}°C 🌡️
Feels like: {FEELS_LIKE:.2f}°C
Min temperature: {TEMP_MIN:.2f}°C
Max temperature: {TEMP_MAX:.2f}°C
Pressure: {PRESSURE} hPa
Humidity: {HUMIDITY}%
Sea Level: {SEA_LEVEL}
Visibility: {VISIBILITY} m 👓
Wind Speed: {WIND_SPEED} m/s
Country: {COUNTRY} {flag.flagize(":" + COUNTRY + ":")}
Sunrise: {SUNRISE} 🌅
Sunset: {SUNSET} 🌇"""

    ARABIC_REPORT = f"""\tالطقس: {DESCRIPTION} 🛰️
درجة الحرارة: {TEMP:.2f}°C 🌡️
درجة الحرارة المرضية: {FEELS_LIKE:.2f}°C
الحرارة الدنيا: {TEMP_MIN:.2f}°C
الحرارة القصوى: {TEMP_MAX:.2f}°C
الضغط: {PRESSURE} hPa
معدل الرطوبة: {HUMIDITY}%
مستوى سطح البحر: {SEA_LEVEL}
مدى الرؤية: {VISIBILITY} m 👓
سرعة الرياح: {WIND_SPEED} m/s
البلد: {COUNTRY} {flag.flagize(":" + COUNTRY + ":")}
وقت الشروق: {SUNRISE} 🌅
وقت الغروب: {SUNSET} 🌇"""

    return ARABIC_REPORT if is_arabic else REPORT