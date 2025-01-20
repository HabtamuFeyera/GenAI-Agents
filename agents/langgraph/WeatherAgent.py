import json
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re

# Initialize DuckDuckGo search client
ddg = DDGS()

# Function to dynamically get Weather.com URL based on the city
def construct_weather_url(city):
    """Construct a Weather.com URL based on the city name."""
    location_codes = {
        "Addis Ababa": "ETXX0002:1:ET",
        "San Francisco": "USCA0987:1:US",
        "London": "UKXX0085:1:UK",
        "New York": "USNY0996:1:US",
        "Tokyo": "JPXX0010:1:JP",
        # Add more cities as needed
    }

    location_code = location_codes.get(city)
    if location_code:
        return f"https://weather.com/weather/today/l/{location_code}"
    else:
        return None

# Search function using DuckDuckGo
def search(query, max_results=1):
    """Perform a DuckDuckGo search and return the top URL, with error handling."""
    try:
        results = ddg.text(query, max_results=max_results)
        if results:
            return results[0]["href"]
        else:
            print("No search results found.")
            return None
    except Exception as e:
        print(f"Error while searching with DuckDuckGo: {e}")
        # Fallback URL if DuckDuckGo fails
        return None

# Function to scrape weather information from the website
def scrape_weather_info(url):
    """Scrape content from the given URL."""
    if not url:
        return "No URL provided for scraping."

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            weather_data = {}

            # Log the HTML content (first 1000 chars) to inspect
            print(f"HTML Content Preview: {response.text[:1000]}")

            # Try to find elements more dynamically and log issues
            temperature = soup.find('span', {'class': re.compile('.*tempValue.*')})
            condition = soup.find('div', {'class': re.compile('.*phraseValue.*')})
            forecast_details = soup.find('div', {'class': re.compile('.*precipValue.*')})

            # Hourly forecast data (if available)
            hourly_forecast = []
            hourly_data = soup.find_all('span', {'class': re.compile('.*extendedData.*')})
            for hour in hourly_data:
                hourly_forecast.append(hour.get_text())

            # Compile the extracted data into a dictionary
            weather_info = {
                "Temperature": temperature.get_text() if temperature else "Not available",
                "Condition": condition.get_text() if condition else "Not available",
                "Forecast": forecast_details.get_text() if forecast_details else "Not available",
                "Hourly Forecast": hourly_forecast[:5]  # Only the next 5 hours
            }

            # Return formatted weather data as a JSON string
            return json.dumps(weather_info, indent=4)
        else:
            return f"Failed to retrieve the webpage. HTTP Status Code: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred while scraping: {e}"

# Function to print raw scraped data
def print_raw_scraped_data(scraped_data):
    """Simply print the raw scraped data."""
    print("Scraped Data:\n")
    print(scraped_data)

# Main function for the Agentic Search flow
def agentic_search(city):
    # Step 1: Construct the Weather URL based on the city
    url = construct_weather_url(city)
    
    if not url:
        return f"Weather URL for {city} not found."

    print(f"Using URL for weather: {url}\n")

    # Step 2: Scrape the weather information from the URL
    scraped_data = scrape_weather_info(url)

    if not scraped_data:
        return "No meaningful data extracted from the website."

    # Step 3: Print the scraped data (formatted as JSON)
    print_raw_scraped_data(scraped_data)

# Example usage
if __name__ == "__main__":
    # Query for weather in Addis Ababa
    query = "What is the current weather in Addis Ababa?"
    agentic_search("Addis Ababa")

    # Query for weather in San Francisco (another example)
    query = "What is the current weather in San Francisco?"
    agentic_search("San Francisco")
