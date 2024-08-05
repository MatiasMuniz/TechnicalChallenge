#!/usr/bin/python3
# Python 3.12.4
from typing import List, Dict, Any
import requests
from functools import reduce

def fetch_all_movie_data(url: str) -> List[Dict[str, Any]]:
    """
    Fetch all movie data from a paginated API.

    Args:
        url (str): The base URL of the paginated API.

    Raises:
        SystemExit: If a request or JSON decode error occurs.
        ValueError: If the response format is unexpected.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing movie data.
    """
    all_data = []
    page = 1
    max_pages = 20
    while page <= max_pages:

        try:
            response = requests.get(f"{url}?page={page}")
            response.raise_for_status()
            data = response.json()
        
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"Request error: {e}")
        
        except ValueError as e:
            raise SystemExit(f"JSON decode error: {e}")
        
        movies = data.get('data', [])
        
        if not isinstance(movies, list):
            raise ValueError("Unexpected response format: 'data' is not a list.")
        
        all_data.extend(movies)
        total_pages = data.get('total_pages', 1)
        
        if not isinstance(total_pages, int):
            raise ValueError("Unexpected response format: 'total_pages' is not an integer.")

        page += 1
        
    return all_data

def best_in_genre(genre: str, data: List[Dict[str, Any]]) -> str:
    """Return the highest-rated show in the given genre.

    Args:
        genre (str): The genre to search for.
        data (List[Dict[str, Any]]): A list of dictionaries containing movie data.

    Raises:
        ValueError: If the input types are invalid.

    Returns:
        str: The name of the highest-rated show in the given genre. If no shows are found, a message is returned.
    """
    if not (isinstance(genre, str) and isinstance(data, list)):
        raise ValueError("Invalid input: genre must be a string and data must be a list.")
    
    filtered_movies = [movie for movie in data if genre.lower() in map(str.lower, movie.get('genre', 'Unknown').split(', '))]

    if not filtered_movies:
        return "No TV series found for the given genre."
    
    best_movie = reduce(
        lambda best, current: current if (-float(current.get('imdb_rating', 0)), current.get('name', '')) < (-float(best.get('imdb_rating', 0)), best.get('name', '')) else best,
        filtered_movies
    )
    
    return best_movie.get('name', 'Unknown')

def main() -> int:
    """Main function to find the best TV series in a given genre."""
    url = "https://jsonmock.hackerrank.com/api/tvseries"
    genre = "Action"
    
    try:
        all_movies = fetch_all_movie_data(url)
        result = best_in_genre(genre, all_movies)
        print(result)
    
    except (ValueError, SystemExit) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()