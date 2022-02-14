import requests


class SearchMovies():
    def __init__(self):
        self.API_KEY = "API KEY FROM THE API_URL"
        self.API_URL = "https://api.themoviedb.org/3/"
        self.INFO_URL = "https://api.themoviedb.org/3/movie"
        self.IMAGE_URL = "https://image.tmdb.org/t/p/w500"

    def get_movies(self, movie_name):
        parameters = {
            "api_key": self.API_KEY,
            "query": movie_name
        }
        response = requests.get(
            f"{self.API_URL}search/movie", params=parameters)
        response.raise_for_status()
        return response.json()

    def get_movie_by_id(self, movie_id):
        parameters = {
            "api_key": self.API_KEY
        }
        response = requests.get(
            f"{self.API_URL}movie/{movie_id}", params=parameters)
        response.raise_for_status()
        json = response.json()
        IMG_URL = f"{self.IMAGE_URL}{json['poster_path']}"
        MOVIE_DESCRIPTION = json['overview']
        TITLE = json['original_title']
        YEAR = json['release_date']
        ESSENTIAL_DATA = {
            "IMG_URL": IMG_URL,
            "DESCRIPTION": MOVIE_DESCRIPTION,
            "TITLE": TITLE,
            "YEAR": YEAR
        }
        return ESSENTIAL_DATA
