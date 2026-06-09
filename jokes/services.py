"""
Service module to interact with JokeAPI
"""
import requests
from django.conf import settings
from django.core.cache import cache
from .models import Joke


def fetch_random_joke():
    """
    Fetch a random joke from JokeAPI
    Returns: dict with joke data or None if request fails
    """
    try:
        url = f"{settings.JOKE_API_BASE_URL}/Any?type=single"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # JokeAPI returns error flag
        if data.get('error'):
            print("JokeAPI returned an error")
            return None
        
        # JokeAPI returns different format, convert to our format
        if data.get('type') == 'single':
            return {
                'setup': data.get('joke', ''),
                'punchline': '',
                'type': data.get('category', 'general').lower()
            }
        else:
            return {
                'setup': data.get('setup', ''),
                'punchline': data.get('delivery', ''),
                'type': data.get('category', 'general').lower()
            }
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
    Fetch a random joke by type from JokeAPI
    Supports types: 'general', 'knock-knock', 'programming'
    Returns: dict with joke data or None if request fails
    """
    try:
        # Map our joke types to JokeAPI categories
        category_map = {
            'general': 'General',
            'knock-knock': 'Knock-Knock',
            'programming': 'Programming'
        }
        
        category = category_map.get(joke_type, 'General')
        url = f"{settings.JOKE_API_BASE_URL}/{category}?type=single"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # JokeAPI returns error flag
        if data.get('error'):
            print(f"JokeAPI returned an error for category {category}")
            return None
        
        # JokeAPI returns different format, convert to our format
        if data.get('type') == 'single':
            joke_data = {
                'setup': data.get('joke', ''),
                'punchline': '',
                'type': joke_type
            }
        else:
            joke_data = {
                'setup': data.get('setup', ''),
                'punchline': data.get('delivery', ''),
                'type': joke_type
            }
        
        # Save to database for history
        Joke.objects.create(
            setup=joke_data.get('setup', ''),
            punchline=joke_data.get('punchline', ''),
            joke_type=joke_data.get('type', joke_type)
        )
        
        return joke_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching joke by type: {e}")
        return None
