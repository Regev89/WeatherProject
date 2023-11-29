import requests
from datetime import datetime
import pytz
import streamlit as st
import pandas as pd
from collections import OrderedDict
import json
import numpy as np


def get_weather(api_key, city, country_code, temp, lat, lng):
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    if temp == 'Celsius':
        units = 'metric'
        units_sign = '°C'
    elif temp == 'Kelvin':
        units = 'standard'
        units_sign = '°K'
    elif temp == 'Fahrenheit':
        units = 'imperial'
        units_sign = '°F'

    params = {
        'q': f'{city},{country_code}',
        'appid': api_key,
        'units': units
    }

    try:
        response = requests.get(base_url, params=params)
        json_data = response.json()

        print(json.dumps(json_data, indent=2))

        if response.status_code == 200:
            # Extract relevant information from the response
            weather_description = json_data['weather'][0]['description']
            weather_icon = json_data['weather'][0]['icon']
            temperature = json_data['main']['temp']
            feels_like = json_data['main']['feels_like']
            humidity = json_data['main']['humidity']
            timezone = json_data.get('timezone', int)
            image_url = f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"

            st.markdown(
                f"## Weather in {city.title()}, {country_code}:")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"#### 🌡️ Temperature:")
                st.markdown(f"### {temperature:.2f}{units_sign}")
                st.markdown(f"#### Feels like:")
                st.markdown(f"### {feels_like:.2f}{units_sign}")

            with col2:
                st.markdown(f"#### Description:")
                st.markdown(f"##### {weather_description.capitalize()}")
                st.image(image_url)
            with col3:
                st.markdown(f"#### Humidity:")
                st.markdown(f"### {humidity}%")

            st.markdown(f"\n\n")
            show_xweather = st.toggle("Extended weather mdoe")
            if (show_xweather):
                st.markdown(f"## More!")

            # print(f"Timezone is: {timezone}")
            print(int(int(timezone)/3600))

            return int(int(timezone)/3600), {"latitude": lat, "longitude": lng, "zoom": 10}
        else:
            print(f"Error: {data['message']}")

    except Exception as e:
        print(f"An error occurred: {e}")
        st.markdown(
            f"We're sorry, it's seems like there is no weather information for {city}.")


def get_datetime_in_timezone(time_difference: int):
    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Calculate the time with the specified difference
    target_timezone = pytz.timezone(
        f'Etc/GMT{"-" if time_difference >= 0 else ""}{time_difference}')
    target_datetime = utc_now.replace(
        tzinfo=pytz.utc).astimezone(target_timezone)

    return target_datetime


api_key = '4d20a4dc273256d2214e0d809460c1dd'

file = "worldcities.csv"
data = pd.read_csv(file)

st.title("Weather App ⛅")


col1, col2 = st.columns(2, gap="medium")
with col1:
    st.subheader("Choose a city from main list")
    country_list = list(data.loc[:, "country"])
    country_list.sort()
    sorted_country_list = OrderedDict.fromkeys(country_list)
    country = st.selectbox(
        'Select a country', options=sorted_country_list, placeholder='Choose a country')

    country_data = data.loc[data.loc[:, "country"] == country, :]

    city_set = country_data.loc[:, "city_ascii"]

    city = st.selectbox('Select a city', options=sorted(city_set))
    lat = float(country_data.loc[data.loc[:, "city_ascii"] == city, "lat"])
    print(lat)
    lng = float(country_data.loc[data.loc[:, "city_ascii"] == city, "lng"])
    country_code_dt = country_data.loc[data.loc[:,
                                                "city_ascii"] == city, "iso2"]
    country_code = country_code_dt.iloc[0]

    # temp = st.selectbox(
    #     'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'))

    temp = st.radio(
        'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'), index=None)

with col2:
    st.subheader("Or choose one a saved city:")


if (temp):
    time_difference, location = get_weather(
        api_key, city, country_code, temp, lat, lng)
    result_datetime = get_datetime_in_timezone(time_difference)

    show_time = st.checkbox('Show current time in selected location')
    if show_time:
        st.markdown(f'#### ⏰ Current date and time in {city} is:')
        st.markdown(
            f'### {result_datetime.strftime("%A, %B %d, %Y, %H:%M %p")}')

    show_map = st.checkbox('Show map')
    if show_map:
        df = pd.DataFrame({
            "col1": np.random.randn(1000) / 50 + lat,
            "col2": np.random.randn(1000) / 50 + lng,
            "col3": np.random.randn(1000) * 100
        })

        st.map(data=df, latitude='col1', longitude='col2',
               size='col3', color='#00000000', zoom=12)

# show_weather = st.button("Show Weather")
# if (show_weather):
#     get_weather(api_key, city, country_code, temp, lat, lng)
