"""
Service module to interact with the Official Joke API
"""
import requests
from django.conf import settings
from django.core.cache import cache
from .models import Joke


def fetch_random_joke():
    """
    Fetch a random joke from the Official Joke API
    Returns: dict with joke data or None if request fails
    """
    try:
        response = requests.get(settings.JOKE_API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke: {e}")
        return None


def get_random_joke():
    """
    Get a random joke and optionally save it to the database
    Returns: dict with joke data or None
    """
    joke_data = fetch_random_joke()
    
    if joke_data:
        # Save to database for history
        Joke.objects.create(
            setup=joke_data.get('setup', ''),
            punchline=joke_data.get('punchline', ''),
            joke_type=joke_data.get('type', 'general')
        )
        return joke_data
    
    return None


def get_random_joke_by_type(joke_type):
    """
    Fetch a random joke by type from the Official Joke API
    Supports types: 'general', 'knock-knock', 'programming'
    Returns: dict with joke data or None if request fails
    """
    try:
        url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # API returns a list for some endpoints
        data = response.json()
        if isinstance(data, list):
            data = data[0]
        
        # Save to database for history
        Joke.objects.create(
            setup=data.get('setup', ''),
            punchline=data.get('punchline', ''),
            joke_type=data.get('type', joke_type)
        )
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke by type: {e}")
        return None
