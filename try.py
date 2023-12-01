import requests
from datetime import datetime
import pytz
import streamlit as st
import pandas as pd
from collections import OrderedDict
import json
import numpy as np


def get_weather(api_key, city, country_code, temp, lat=0, lng=0):
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


def switch_source(source):
    if source == "col1":
        st.session_state["table_select_box"] = None
    elif source == "col2":
        st.session_state["country_selectbox"] = None


def switch_to_table(city):
    st.session_state["country_selectbox"] = None
    st.session_state["table_select_box"] = city


def switch_to_main(country):
    st.session_state["table_select_box"] = None
    st.session_state["country_selectbox"] = country


api_key = '4d20a4dc273256d2214e0d809460c1dd'

file = "worldcities.csv"
data = pd.read_csv(file)

st.title("Weather App ⛅")
st.session_state.show_details = False
from_table = False
temp = None

if ("country_selectbox" not in st.session_state):
    st.session_state["country_selectbox"] = None
if ("table_select_box" not in st.session_state):
    st.session_state["table_select_box"] = None

st.write(st.session_state)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader("Choose a city")
    country_list = list(data.loc[:, "country"])
    country_list.sort()
    sorted_country_list = OrderedDict.fromkeys(country_list)
    country = st.selectbox(
        'Select a country', options=sorted_country_list, placeholder='Choose a country', key="country_selectbox", index=None)

    if (country):
        # switch_source("col1")
        country_data = data.loc[data.loc[:, "country"] == country, :]
        city_set = country_data.loc[:, "city_ascii"]
        city = st.selectbox('Select a city', options=sorted(
            city_set), placeholder='Choose a city', index=0)
        country_code_dt = country_data.loc[data.loc[:,
                                                    "city_ascii"] == city, "iso2"]
        country_code = country_code_dt.iloc[0]

        if (city):
            lat = float(
                country_data.loc[data.loc[:, "city_ascii"] == city, "lat"])
            lng = float(
                country_data.loc[data.loc[:, "city_ascii"] == city, "lng"])
            from_table = False

            temp = st.radio(
                'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'), index=None, key="main_radio")


with col2:
    st.subheader("Or choose a saved city:")
    # st.table(saved_cities_table)
    ex_user_table = {"City": ['Barcelona', 'Tel Aviv', 'Delhi'],
                     "Country": ['Spain', 'Israel', 'India'],
                     "Time Zone": ['+1:00 UTC', '+2:00 UTC', '+5:30 UTC'],
                     "Country Code": ['ES', 'IL', 'IN'],
                     "Lat": ['41.390', '32.068', '28.644'],
                     "Lng": ['2.154', '34.785', '77.216']}

    dt = pd.DataFrame(ex_user_table)
    dt_section = dt.loc[:, ["City", "Country", "Time Zone"]]
    st.table(dt_section)

    city_from_table = st.selectbox('Select a city from table', options=sorted(
        dt_section["City"]), placeholder='Choose a city', index=st.session_state["table_select_box"], key="table_select_box", on_change=switch_to_table)

    if (city_from_table):
        # switch_source("col2")
        for i, table_city in enumerate(ex_user_table["City"]):
            print(i, table_city)

            if table_city == city_from_table:
                saved_index = i
        country_code_from_table = ex_user_table["Country Code"][saved_index]
        from_table = True
        temp = st.radio(
            'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'), index=None, key="saved radio")

# main window
if (temp):
    st.session_state.show_details = True

if (st.session_state.show_details):
    if (from_table):
        time_difference = get_weather(
            api_key, city_from_table, country_code_from_table, temp)
        location = {"latitude": float(ex_user_table["Lat"][saved_index]),
                    "longitude": float(ex_user_table["Lng"][saved_index]), "zoom": 10}
    else:
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
            "col1": np.random.randn(1000) / 50 + location['latitude'],
            "col2": np.random.randn(1000) / 50 + location['longitude'],
            "col3": np.random.randn(1000) * 100
        })

        st.map(data=df, latitude='col1', longitude='col2',
               size='col3', color='#00000000', zoom=12)

# show_weather = st.button("Show Weather")
# if (show_weather):
#     get_weather(api_key, city, country_code, temp, lat, lng)
