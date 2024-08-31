import requests
import collections
from functools import reduce
from typing import List, Dict, Any

# Define a namedtuple called 'Movie' with fields 'name', 'imdb_rating', and 'genre'.
Movie = collections.namedtuple('Movie', ['name', 'imdb_rating', 'genre'])

class Movies:
    """
    A class to represent a collection of movies fetched from an API.

    Attributes:
        _movies (List[Movie]): A list of Movie namedtuples representing the movies fetched from the API.

    Methods:
        request_movies() -> List[Dict[str, Any]]:
            Static method that fetches movie data from the paginated API.
    """

    def __init__(self):
        self._movies = [Movie(movie['name'], movie['imdb_rating'], movie['genre'].split(", "))  for movie in self.request_movies()]

    @staticmethod
    def request_movies() -> List[Dict[str, Any]] | None:
        all_movies = []
        max_pages = 1
        page = 1
        url = "https://jsonmock.hackerrank.com/api/tvseries"

        while page <= max_pages:
            try:
                response = requests.get(f"{url}?page={page}").json()["data"]
                all_movies.extend(response)
                page += 1

            except requests.exceptions.RequestException as e:
                raise SystemExit(f"Request error: {e}")

            except ValueError as e:
                raise SystemExit(f"JSON decode error: {e}")

        return all_movies

    def get_filter_movies(self, genre: str) -> List[Movie]:
        filtered_movies = [movie for movie in self._movies if genre in movie.genre]
        return filtered_movies or "No TV series found for the given genre."

    def get_best_movie(self, genre: str) -> Movie | str:
        filtered_movies = self.get_filter_movies(genre)
        best_movie = reduce(lambda best, current: current if (-float(current.imdb_rating), current.name) < (-float(best.imdb_rating), best.name) else best,  filtered_movies)
        return best_movie

def main() -> Movie | None:
    movies = Movies()
    best_movie = movies.get_best_movie("Action")

    print(best_movie)

if __name__ == '__main__':
    main()