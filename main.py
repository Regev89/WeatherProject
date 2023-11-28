import requests
from datetime import datetime
import pytz
import streamlit as st

cities_list = []
cities_list.append(('Tokyo', 'Japan'))
cities_list.append(('Buenos Aires', 'Argentina'))
cities_list.append(('Tel Aviv', 'Israel'))
cities_list.append(('Rome', 'Italy'))
cities_list.sort()

country_codes = {
    "Afghanistan": "AF",
    "Albania": "AL",
    "Algeria": "DZ",
    "Andorra": "AD",
    "Angola": "AO",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bhutan": "BT",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "Brunei": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO",
    "Comoros": "KM",
    "Congo": "CG",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Eswatini": "SZ",
    "Ethiopia": "ET",
    "Fiji": "FJ",
    "Finland": "FI",
    "France": "FR",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Greece": "GR",
    "Grenada": "GD",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Honduras": "HN",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Laos": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mexico": "MX",
    "Micronesia": "FM",
    "Moldova": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar (Burma)": "MM",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "North Korea": "KP",
    "North Macedonia": "MK",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Qatar": "QA",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Vincent and the Grenadines": "VC",
    "Samoa": "WS",
    "San Marino": "SM",
    "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Suriname": "SR",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Taiwan": "TW",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Togo": "TG",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Tuvalu": "TV",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom": "GB",
    "United States": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Vanuatu": "VU",
    "Vatican City": "VA",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Yemen": "YE",
    "Zambia": "ZM",
    "Zimbabwe": "ZW",
}

my_API = '4d20a4dc273256d2214e0d809460c1dd'

def get_weather(api_key, city,country_code):
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': f'{city},{country_code}',
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        # print (json.dumps(data, indent = 2))

        if response.status_code == 200:
            # Extract relevant information from the response
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            timezone = data.get('timezone', None)

            print(f"Weather in {city.title()}, {country_code}:")
            print(f"Description: {weather_description}")
            print(f"Temperature: {temperature:.2f}°C")
            print(f"Humidity: {humidity}%")
            
            st.markdown(f"## Weather in {city.title()}, {country_code}:")
                
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Temperature: {temperature:.2f}°C")

            with col2:
                st.write(f"Description: {weather_description.capitalize()}")

            with col3:
                st.write(f"Humidity: {humidity}%")
            
            
            
            # print(f"Timezone is: {timezone}")
            return int(timezone/3600)
        else:
            print(f"Error: {data['message']}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def get_datetime_in_timezone(time_difference):
    # Get the current UTC time
    utc_now = datetime.utcnow()
    user_time = datetime.now(pytz.timezone('Israel'))
    formatted_user_time = user_time.strftime("%A, %B %d, %Y, %H:%M %p")
    print(f"Your current date and time: {formatted_user_time}")

    # Calculate the time with the specified difference
    target_timezone = pytz.timezone(f'Etc/GMT{"-" if time_difference >= 0 else ""}{time_difference}')
    target_datetime = utc_now.replace(tzinfo=pytz.utc).astimezone(target_timezone)

    return target_datetime

def save_new_city(city, country_code):
    global cities_list
    cities_list.append((city, country_code))
    print(cities_list)
    st.text('Saved successfully')
    

def new_city():
    st.markdown("# Weather App")
    st.markdown("## <span style='color:#000080;'>Regev Ace</span>", unsafe_allow_html=True)
    st.text('Created as a python project for Data Science study')
    st.markdown("<span style='border-bottom: 5px solid green;'></span>", unsafe_allow_html=True)

    
    # 1 - city
    city = st.text_input('Enter your requested city: ')
    if city:
        # 2 - country
        country = st.selectbox('Please choose a country from the list below:', options= country_codes.keys(), placeholder="Choose a country",index=None)
        if country is not None:
            country_code = country_codes[country]
            time_difference = get_weather(api_key, city, country_code)
            result_datetime = get_datetime_in_timezone(time_difference)
            try:
                # Print the result with the custom strftime format
                print(f"Current date and time in {city} is:")
                print(result_datetime.strftime("%A, %B %d, %Y, %H:%M %p"))
                st.markdown(f'## {result_datetime.strftime("%A, %B %d, %Y, %H:%M %p")}')
                
            except ValueError:
                print("Invalid input. Please enter a valid number.") 
            
            save_button = st.button("Save City")
            if (save_button):
                save_new_city(city, country_code)
                country = None
    

def saved_cities():
    st.title('Please Choose a city from the list: ')
    print (cities_list)
    selected_city = st.selectbox(" ",options=[city [0] for city in cities_list], placeholder="Choose a city",
                                 index=None, label_visibility="hidden")
    if selected_city is not None:
        for city in cities_list:
            if selected_city in city:
                selected_city_county_code = country_codes[city[1]]
        get_weather(my_API, selected_city, selected_city_county_code)
        



if __name__ == "__main__":
    api_key = my_API
    with st.sidebar:
        st.title('Quick Menu')
        selected = st.sidebar.selectbox("Please Choose one of the following optoins: ", ("New City", "Saved Cities"), 
                                        placeholder="Choose an option", index=None)
    match selected:
        case 'New City': new_city()
        case 'Saved Cities': saved_cities()
        
    
    # type_city(input ('Would you like to check the weather in a city? (Y/N): '))
    
