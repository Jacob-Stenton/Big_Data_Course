import requests
import pandas
import random
import os
import time

API_KEY = "d3d26f516ed5ae7c80a6af8877674c77"
OUTPUT_FILE = "/home/joshmurr/weather.csv"

def getLatLon():
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    return lat, lon

while True:
    lat, lon = getLatLon()

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat:.5f}&lon={lon:.5f}&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()

    print(f"Response for lat: {lat}, lot: {lon} recieved with status: {response.status_code}")

    df = pandas.json_normalize(data)
    df.to_csv(OUTPUT_FILE, mode='a', header=not os.path.exists(OUTPUT_FILE))

    time.sleep(120) # Wait 2 minutes



