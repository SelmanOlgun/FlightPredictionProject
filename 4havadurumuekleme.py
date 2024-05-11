import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

BASE_URL = "https://api.weatherapi.com/v1/history.json?"
API_KEY = "b499c65dd84846b6a32185627240905"
csv_file_path = "3bossatirlarisilinmis.csv"
output_csv_path = "4havadurumueklenmis.csv"

df = pd.read_csv(csv_file_path)

new_columns = [
    'ORIGIN_CITY_MAXTEMP_C',
    'ORIGIN_CITY_MINTEMP_C',
    'ORIGIN_CITY_AVGTEMP_C',
    'ORIGIN_CITY_MAXWIND_KPH',
    'ORIGIN_CITY_TOTALPRECIP_MM',
    'ORIGIN_CITY_AVGVIS_KM',
    'ORIGIN_CITY_AVGHUMIDITY',
    'ORIGIN_CITY_TEXT',
    'ORIGIN_CITY_DAILY_CHANCE_OF_RAIN',
    'ORIGIN_CITY_DAILY_CHANCE_OF_SNOW',
    'DEST_CITY_MAXTEMP_C',
    'DEST_CITY_MINTEMP_C',
    'DEST_CITY_AVGTEMP_C',
    'DEST_CITY_MAXWIND_KPH',
    'DEST_CITY_TOTALPRECIP_MM',
    'DEST_CITY_AVGVIS_KM',
    'DEST_CITY_AVGHUMIDITY',
    'DEST_CITY_TEXT',
    'DEST_CITY_DAILY_CHANCE_OF_RAIN',
    'DEST_CITY_DAILY_CHANCE_OF_SNOW'
]

for col in new_columns:
    df[col] = ""

def get_forecast(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_data = data['forecast']['forecastday'][0]['day']
        return {
            'MAXTEMP_C': forecast_data['maxtemp_c'],
            'MINTEMP_C': forecast_data['mintemp_c'],
            'AVGTEMP_C': forecast_data['avgtemp_c'],
            'MAXWIND_KPH': forecast_data['maxwind_kph'],
            'TOTALPRECIP_MM': forecast_data['totalprecip_mm'],
            'AVGVIS_KM': forecast_data['avgvis_km'],
            'AVGHUMIDITY': forecast_data['avghumidity'],
            'TEXT': forecast_data['condition']['text'],
            'DAILY_CHANCE_OF_RAIN': forecast_data['daily_chance_of_rain'],
            'DAILY_CHANCE_OF_SNOW': forecast_data['daily_chance_of_snow']
        }
    else:
        print(f"Hata kodu: {response.status_code} - URL: {url}")
        return None

def process_row(row):
    date = row['FL_DATE']
    origin_city = row['ORIGIN_CITY']
    dest_city = row['DEST_CITY']

    origin_url = f"{BASE_URL}key={API_KEY}&q={origin_city}&dt={date}"
    dest_url = f"{BASE_URL}key={API_KEY}&q={dest_city}&dt={date}"

    origin_forecast = get_forecast(origin_url)
    dest_forecast = get_forecast(dest_url)

    return origin_forecast, dest_forecast

def update_dataframe(result, index, prefix):
    if result:
        for key, value in result.items():
            df.at[index, f'{prefix}_{key}'] = value

chunk_size = 1000

with tqdm(total=len(df)) as pbar:
    with ThreadPoolExecutor() as executor:
        futures = []
        for index, row in df.iterrows():
            future = executor.submit(process_row, row)
            future.add_done_callback(lambda p: pbar.update())
            futures.append((future, index))

        for future, index in futures:
            origin_forecast, dest_forecast = future.result()
            update_dataframe(origin_forecast, index, 'ORIGIN_CITY')
            update_dataframe(dest_forecast, index, 'DEST_CITY')

df.to_csv(output_csv_path, index=False)
print("Dosya oluşturuldu:", output_csv_path)
