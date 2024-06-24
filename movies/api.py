import requests

def fetch_movies(api_key, query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    response = requests.get(url)
    return response.json()

def fetch_tv_series(api_key, query):
    url = f'https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={query}'
    response = requests.get(url)
    return response.json()

def fetch_cartoon_movies(api_key, genre_id=16):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}'
    response = requests.get(url)
    return response.json()