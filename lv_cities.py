import requests
from collections import Counter
from bs4 import BeautifulSoup
import re

def fetch_latvian_cities():
    """
    Fetches list of Latvian cities from Wikipedia
    """
    url = "https://en.wikipedia.org/wiki/List_of_cities_in_Latvia"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table with cities
    cities = []
    tables = soup.find_all('table', {'class': 'wikitable'})
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if cells:
                # Get city name from first column
                city_name = cells[0].text.strip().split()[0]
                # Remove any parentheses and content within
                #city_name = re.sub(r'\([^)]*\)', '', city_name)
                # Clean up any remaining special characters
                #city_name = re.sub(r'[^a-zA-Z\s]', '', city_name)
                cities.append(city_name)
    
    return cities

def analyze_endings(cities):
    """
    Analyzes the two-letter endings of city names and returns most common
    """
    endings = []
    for city in cities:
        if len(city) >= 2:
            endings.append(city[-2:].lower())
    
    # Count frequencies
    ending_counts = Counter(endings)
    return ending_counts

def main():
    try:
        # Fetch cities
        print("Fetching Latvian cities...")
        cities = fetch_latvian_cities()
        
        if not cities:
            print("No cities found!")
            return
            
        print(f"\nFound {len(cities)} cities.")
        print("\nAnalyzing endings...")
        
        # Analyze endings
        ending_counts = analyze_endings(cities)
        
        # Print results
        print("\nMost common two-letter endings:")
        for ending, count in ending_counts.most_common():
            print(f"'{ending}': {count} cities")
            
        # Print example cities for most common ending
        most_common_ending = ending_counts.most_common(1)[0][0]
        print(f"\nExamples of cities ending in '{most_common_ending}':")
        examples = [city for city in cities if city.lower().endswith(most_common_ending)]
        print(", ".join(examples[:5]))
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
