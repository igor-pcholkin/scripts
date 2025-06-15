import requests
from collections import Counter
from bs4 import BeautifulSoup

def fetch_latvian_cities():
    url = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Latvia"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    cities = []
    table = soup.find("table", {"class": "wikitable"})
    
    if table:
        rows = table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            columns = row.find_all("td")
            if columns:
                city_name = columns[0].text.strip()
                cities.append(city_name)
    
    return cities

def find_most_frequent_suffixes(cities):
    suffix_counter = Counter(city[-2:] for city in cities if len(city) >= 2)
    
    most_common = suffix_counter.most_common(1)
    return most_common[0] if most_common else None

if __name__ == "__main__":
    cities = fetch_latvian_cities()
    
    most_frequent_suffix = find_most_frequent_suffixes(cities)
    
    if most_frequent_suffix:
        print(f"Most frequent 2-letter ending: {most_frequent_suffix[0]} (Count: {most_frequent_suffix[1]})")
    else:
        print("No valid data found.")
