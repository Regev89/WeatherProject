# Weather App

## Overview

The Weather App is a simple Python application that provides current weather information for cities around the world. It utilizes the OpenWeatherMap API to fetch real-time weather data. The user can input the city and country through three different methods: selecting from a list, choosing from a set of saved cities, or free-text input.

## Files

- **main.py**: The main file that contains the application code.
- **worldcities.csv**: A CSV file containing a vast list of cities from around the world.
- **country_codes.py**: A Python file with a dictionary mapping countries to their respective ISO2 country codes.
- **requirements.txt**: A standard file for packages used in this app.

## Features

1. **Select from Dropdowns**: Choose the country and city from dropdown select boxes to get the weather information.
2. **Saved Cities List**: Select from a small list of pre-saved cities for quick access to their weather details.
3. **Free Text Input**: Enter the city and country manually for flexibility in searching.

## Future Features
1. Save a city to the list of saved cities after searching that city - that feature now works!
2. Get extendend information about selected city with from provided Json.

## How to Use
The app will lunch with a sidebar asking for your favorite method to search for a city of your choice.

1. **Select from Dropdowns:**
   - Choose the country and city from the provided select boxes.
   
2. **Saved Cities List:**
   - Select a city from the saved cities list as shown in table.

3. **Free Text Input:**
   - Enter the city and country in the input fields.
  
After selecting your preferred temperature unit the information will pop on the screen automatically.

## Dependencies

- Python 3.x
- Requests library (install using `pip install requests`)
- Datetime library (built-in)
- Pytz library (install using `pip install pytz`)
- Streamlit library (install using `pip install streamlit`)
- Pandas library (install using `pip install pandas`)
- Collections module (built-in)
- JSON module (built-in)
- NumPy library (install using `pip install numpy`)

## How to Run

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Run `main.py` using a Python interpreter.
* You can also run as a localhost at streamlit: 'streamlit run main.py'

Here is a link to the app on streamlit: `https://weatherproject-ir8gryucmhdqksnrecdflo.streamlit.app/`

## Acknowledgments
Thanks to OpenWeatherMap for providing the weather data API.
