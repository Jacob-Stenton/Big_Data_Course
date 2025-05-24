import random
import os


import pandas
import requests


# this should be a week04/open_weather_key.py file created by you, containing your API key for the Open Weather Map platform
# API_KEY = "XYZ"
# If you don't have one, create a free Open Weather Map account and generate an API key here: https://home.openweathermap.org/api_keys
# You should be able to create a free account for API v2 (no need to give your payment details)
from week04.open_weather_key import API_KEY

## Add your output file location below
OUTPUT_FILE = "weather_data.csv"

lon = random.uniform(-180, 180)
lat = random.uniform(-90, 90)
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat:.5f}&lon={lon:.5f}&appid={API_KEY}"

response = requests.get(url)
data = response.json()

df = pandas.json_normalize(data)
df.to_csv(OUTPUT_FILE, mode='a', header=not os.path.exists(OUTPUT_FILE))


