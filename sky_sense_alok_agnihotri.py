import requests
from colorama import Fore, Style

API_KEY = '#Enter your API key here#'
BASE_URL = '#Enter your base URL here#'

def get_weather_forecast(city_name, print_current_forecast=False):
    """
    Get the weather forecast for a single city.
    """
    url = f"{BASE_URL}weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = response.json()

        weather = data['weather'][0]
        main_weather = weather['main']
        description = weather['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        temperature_celsius = temperature - 273.15
        forecast = f"City: {city_name}\nWeather: {main_weather} ({description})\nTemperature: {temperature_celsius:.2f}°C\nHumidity: {humidity}%"

        if print_current_forecast:
            print("\nFetching current forecast...\n")

        return forecast
    except requests.exceptions.RequestException as e:
        return f"Unable to fetch weather data for {city_name}. Error: {str(e)}"


def get_extended_forecast(city_name):
    """
    Get the extended weather forecast for a single city.
    """
    url = f"{BASE_URL}forecast?q={city_name}&appid={API_KEY}"
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = response.json()

        forecast = ""
        for item in data['list']:
            date_time = item['dt_txt']
            weather = item['weather'][0]
            main_weather = weather['main']
            description = weather['description']
            temperature = item['main']['temp']
            humidity = item['main']['humidity']
            temperature_celsius = temperature - 273.15

            forecast += f"Date/Time: {date_time}\nWeather: {main_weather} ({description})\nTemperature: {temperature_celsius:.2f}°C\nHumidity: {humidity}%\n\n"

        return forecast
    except requests.exceptions.RequestException as e:
        return f"Unable to fetch extended forecast data for {city_name}. Error: {str(e)}"


def get_multiple_weather_forecast(cities):
    """
    Get the weather forecast for multiple cities.
    """
    forecasts = []
    for city in cities:
        forecast = get_weather_forecast(city)
        forecasts.append(forecast)
    return forecasts


def get_multiple_extended_forecast(cities):
    """
    Get the extended weather forecast for multiple cities.
    """
    extended_forecasts = []
    for city in cities:
        extended_forecast = get_extended_forecast(city)
        extended_forecasts.append(extended_forecast)
    return extended_forecasts


def display_forecast(city, forecast):
    """
    Display the forecast for a city.
    """
    print(f"\nCity: {city}")
    print("\n")
    print(forecast)


def main():
    print("\n")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + Style.DIM + "\033[4m" + "\t\t\t\t\t\t\tWelcome to the Sky Sense Weather Forecast Application!")
    print("\t\t\t\t\t\t\t------------------------------------------------------" + Style.RESET_ALL)
    print("\n")

    while True:
        print("\nSelect an option:\n")
        print("1. Single city weather forecast")
        print("2. Multiple cities weather forecast")
        print("3. Exit")

        option = input("\nEnter your choice (1, 2, or 3): ")

        if option == '1':
            city = input("\nEnter the city name: ")
            forecast_type = input("Enter the forecast type (current or extended): ")

            if forecast_type.lower() not in ["current", "extended"]:
                print("Invalid forecast type. Please try again.")
                continue

            if forecast_type.lower() == "current":
                forecast = get_weather_forecast(city, print_current_forecast=True)
                print("\n")
                print(forecast)
            elif forecast_type.lower() == "extended":
                print("Fetching extended forecast...\n")
                extended_forecast = get_extended_forecast(city)
                print("\n")
                print(extended_forecast)
            else:
                print("Invalid forecast type. Please try again.")

        elif option == '2':
            cities = input("Enter the city names separated by commas: ").split(',')
            forecast_type = input("Enter the forecast type (current or extended): ")

            if forecast_type.lower() not in ["current", "extended"]:
                print("Invalid forecast type. Please try again.")
                continue

            if forecast_type.lower() == "current":
                print("Fetching current forecast...\n")
                forecasts = get_multiple_weather_forecast(cities)
                for i, forecast in enumerate(forecasts):
                    display_forecast(cities[i], forecast)
            elif forecast_type.lower() == "extended":
                print("Fetching extended forecast...\n")
                extended_forecasts = get_multiple_extended_forecast(cities)
                for i, extended_forecast in enumerate(extended_forecasts):
                    display_forecast(cities[i], extended_forecast)
                    if not extended_forecast:
                        print("Unable to fetch extended forecast for this city.")
            else:
                print("Invalid forecast type. Please try again.")

        elif option == '3':
            print("\n" + Fore.LIGHTBLUE_EX + Style.BRIGHT + Style.DIM + "\033[4m" + "\t\t\t\t\t\tThank you for using the Sky Sense Weather Forecast Application. Goodbye!")
            print("\t\t\t\t\t\t------------------------------------------------------------------------" + Style.RESET_ALL)
            print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t" + Fore.LIGHTBLUE_EX + Style.BRIGHT + Style.DIM + "\033[4m" + "Developed by Alok Agnihotri" + Style.RESET_ALL + "\n\n")
            break

        else:
            print("Invalid option selected. Please try again.")


if __name__ == "__main__":
    main()
