import requests
from datetime import datetime
import pytz
import streamlit as st
import pandas as pd
from collections import OrderedDict
import json
import numpy as np
import country_codes as cc

# Get data from csv
file = "worldcities.csv"
data = pd.read_csv(file)

# Set variables
if "show_details" not in st.session_state:
    st.session_state.show_details = False

ex_user_table = {"City": ['Barcelona', 'Tel Aviv', 'Delhi'],
                 "Country": ['Spain', 'Israel', 'India'],
                 "Time Zone": ['+1:00 UTC', '+2:00 UTC', '+5:30 UTC'],
                 "Country Code": ['ES', 'IL', 'IN'],
                 "Lat": ['41.390', '32.068', '28.644'],
                 "Lng": ['2.154', '34.785', '77.216']}

# API
api_key = '4d20a4dc273256d2214e0d809460c1dd'

# Functions


def save_new_city(city, country, time_difference,
                  country_code, lat, lng):
    # Sould be WRITEN to a file and not to a variable or the code will always reset the variable when rerun the app
    ex_user_table["City"].append(city)
    ex_user_table["Country"].append(country)
    if time_difference > 0:
        ex_user_table["Time Zone"].append(f'+{time_difference}:00 UTC')
    elif time_difference < 0:
        ex_user_table["Time Zone"].append(f'-{time_difference}:00 UTC')
    else:
        ex_user_table["Time Zone"].append('0:00 UTC')
    ex_user_table["Country Code"].append(country_code)
    ex_user_table["Lat"].append(lat)
    ex_user_table["Lng"].append(lng)
    print(ex_user_table)

    st.text('This fiture will be added soon')


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

            st.markdown("***")
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

            show_xweather = st.toggle("Extended weather mdoe")
            if (show_xweather):
                st.markdown("***")
                st.markdown(f"## More!")

            return int(int(timezone)/3600), {"latitude": lat, "longitude": lng, "zoom": 10}
        else:
            st.markdown(
                f"We're sorry, it's seems like there is no weather information for {city}.")
            print(f"Error: {data['message']}")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_datetime_in_timezone(time_difference: int):
    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Calculate the time with the specified difference
    target_timezone = pytz.timezone(
        f'Etc/GMT{"-" if time_difference >= 0 else ""}{time_difference}')
    target_datetime = utc_now.replace(
        tzinfo=pytz.utc).astimezone(target_timezone)

    return target_datetime


# main screen
st.title("My Humble Weather App ⛅")
st.markdown("#### Created by <span style='color:#000080;'>Regev Ace</span>",
            unsafe_allow_html=True)
st.text('This app is the first python project for Data Science study')
st.markdown("***")

# The Sidebar
with st.sidebar:
    st.title("Menu")
    add_radio = st.radio(
        "How would you like to search?",
        ("City from list", "Saved cities", "Free search"), key="radio"
    )

# Main Screen after choosing from sidebar radio

# Option 1 - List
if st.session_state['radio'] == "City from list":
    st.session_state.show_details = False
    # City from list
    st.subheader("Choose a city")
    country_list = list(data.loc[:, "country"])
    country_list.sort()
    sorted_country_list = OrderedDict.fromkeys(country_list)
    country = st.selectbox(
        'Select a country', options=sorted_country_list, placeholder='Choose a country', key="country_selectbox", index=None)

    if (country):
        country_data = data.loc[data.loc[:, "country"] == country, :]
        city_set = country_data.loc[:, "city_ascii"]
        city = st.selectbox('Select a city', options=sorted(
            city_set), placeholder='Choose a city', index=0, key="city_selectbox")
        country_code_dt = country_data.loc[data.loc[:,
                                                    "city_ascii"] == city, "iso2"]
        country_code = country_code_dt.iloc[0]

        if (city):
            lat = float(
                country_data.loc[data.loc[:, "city_ascii"] == city, "lat"])
            lng = float(
                country_data.loc[data.loc[:, "city_ascii"] == city, "lng"])
            temp = st.radio(
                'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'), index=None, key="deg_radio")
            if (temp):
                time_difference, location = get_weather(
                    api_key, city, country_code, temp, lat, lng)
                result_datetime = get_datetime_in_timezone(time_difference)
                st.session_state.show_details = True

# Option 2 - Saved
elif st.session_state['radio'] == "Saved cities":
    st.session_state.show_details = False
    st.subheader("Choose a saved city:")
    # st.table(saved_cities_table)

    dt = pd.DataFrame(ex_user_table)
    dt_section = dt.loc[:, ["City", "Country", "Time Zone"]]
    st.table(dt_section)

    city_from_table = st.selectbox('Select a city from table', options=sorted(
        dt_section["City"]), placeholder='Choose a city', index=None, key="table_select_box", )

    if (city_from_table):
        city = city_from_table
        # switch_source("col2")
        for i, table_city in enumerate(ex_user_table["City"]):
            if table_city == city_from_table:
                saved_index = i
        country_code_from_table = ex_user_table["Country Code"][saved_index]
        temp = st.radio(
            'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'), index=None, key="saved radio")
        if (temp):
            time_difference_topple = get_weather(
                api_key, city_from_table, country_code_from_table, temp)
            time_difference = time_difference_topple[0]
            location = {"latitude": float(ex_user_table["Lat"][saved_index]),
                        "longitude": float(ex_user_table["Lng"][saved_index]), "zoom": 10}
            result_datetime = get_datetime_in_timezone(time_difference)
            st.session_state.show_details = True

# Option 3 - Free
elif st.session_state['radio'] == "Free search":
    st.session_state.show_details = False
    st.markdown("<span style='border-bottom: 5px solid green;'></span>",
                unsafe_allow_html=True)

    city = st.text_input('Enter your requested city: ', key="city input")
    if city:
        country = st.text_input(
            'Enter a country name or code (two letters): ', key="country input")
        city = city.capitalize()
        if country:
            if country.title() in cc.country_codes.keys() or country.upper() in cc.country_codes.values():
                if len(country) != 2:
                    country_code = cc.country_codes[country.title()]
                    country = country.title()
                else:
                    country_code = country.upper()
                    country = list(cc.country_codes.keys())[list(
                        cc.country_codes.values()).index(country_code)]

                # Every row where country code like is as choosen, Every column `DF[row([bool]), column(:)]`
                country_data = data.loc[data.loc[:, "iso2"] == country_code, :]

                # Checking whether the Series {country_data.city} has a value equals to {city}
                if city in country_data.city.values:
                    lat = float(
                        country_data.loc[data.loc[:, "city_ascii"] == city, "lat"])
                    lng = float(
                        country_data.loc[data.loc[:, "city_ascii"] == city, "lng"])
                    temp = st.radio(
                        'Select temperature units', options=('Celsius', 'Kelvin', 'Fahrenheit'), index=None, key="Free radio")
                    if (temp):
                        time_difference, location = get_weather(
                            api_key, city, country_code, temp, lat, lng)
                        result_datetime = get_datetime_in_timezone(
                            time_difference)
                        st.session_state.show_details = True

                        # Save button
                        save_button = st.button("Save City")
                        if (save_button):
                            save_new_city(city, country, time_difference,
                                          country_code, lat, lng)

                else:
                    st.markdown(
                        f"We're sorry, it's seems like there is no city called {city} in {country}.")
            else:
                st.markdown(
                    f"We're sorry, it's seems like the country name or code you typed is incorrect.")


# Data Display
if (st.session_state.show_details):
    st.markdown("***")
    show_time = st.checkbox('Show current time in selected location')
    if show_time:
        st.markdown(f'#### ⏰ Current date and time in {city} is:')
        st.markdown(
            f'{result_datetime.strftime("%A, %B %d, %Y, %H:%M %p")}')
        st.markdown("***")

    # np.random.randn(1000) / 50 +  size='col3'
    show_map = st.checkbox('Show map')
    if show_map:
        df = pd.DataFrame({
            "col1": location['latitude'],
            "col2":location['longitude']
            # "col3": np.random.randn(1000) * 100
        })

        st.map(data=df, latitude='col1', longitude='col2',
              color='#00000000', zoom=12)
        st.markdown("***")

# st.write(st.session_state)
