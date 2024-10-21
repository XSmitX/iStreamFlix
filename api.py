import requests

# Replace 'your_api_key' with your actual TMDb API key
API_KEY = '08b12d552c7f37a991383e82161e9db4'
BASE_URL = 'https://api.themoviedb.org/3'

def search_movie_or_tv(query):
    search_url = f"{BASE_URL}/search/multi"
    params = {
        'api_key': API_KEY,
        'query': query
    }
    response = requests.get(search_url, params=params)
    results = response.json().get('results', [])
    
    if results:
        result = results[0]  # Only process the first result
        media_type = result.get('media_type')
        
        if media_type == 'movie':
            movie_details = get_movie_details(result.get('id'))
            return movie_details
        elif media_type == 'tv':
            tv_details = get_tv_details(result.get('id'))
            return tv_details
    else:
        return {"error": "No results found."}

def get_movie_details(movie_id):
    movie_url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY
    }
    response = requests.get(movie_url, params=params)
    movie = response.json()

    return {
        "type": "movie",
        "id": movie.get('id'),
        "title": movie.get('title'),
        "release_date": movie.get('release_date'),
        "overview": movie.get('overview')
    }

def get_tv_details(tv_id):
    tv_url = f"{BASE_URL}/tv/{tv_id}"
    params = {
        'api_key': API_KEY
    }
    response = requests.get(tv_url, params=params)
    tv_show = response.json()

    seasons_info = [
        {
            "season_number": season.get('season_number'),
            "episode_count": season.get('episode_count')
        }
        for season in tv_show.get('seasons', [])
        if season.get('season_number') > 0  # Only include seasons greater than 0
    ]

    return {
        "type": "tv",
        "id": tv_show.get('id'),
        "name": tv_show.get('name'),
        "number_of_seasons": tv_show.get('number_of_seasons'),
        "number_of_episodes": tv_show.get('number_of_episodes'),
        "overview": tv_show.get('overview'),
        "seasons": seasons_info
    }

# Example usage

