import requests
import collections
from functools import reduce

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
    def request_movies():
        all_movies = []
        max_pages = 20
        page = 1
        url = "https://jsonmock.hackerrank.com/api/tvseries"
        
        while page <= max_pages:
            all_movies.extend(requests.get(f"{url}?page={page}").json()["data"])
            page += 1
    
        return all_movies

def main():
    movies = Movies()
    genre = "Action" 
  
    filtered_movies = [movie for movie in movies._movies if genre in movie.genre]
    best_movie = reduce(lambda best, current: current if (-float(current.imdb_rating), current.name) < (-float(best.imdb_rating), best.name) else best,  filtered_movies)
    
    print(best_movie.name)

if __name__ == '__main__':
    main()