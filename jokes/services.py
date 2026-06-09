"""
Service module for fetching various entertainment and wellness content
"""
import requests
import random
from django.conf import settings
from django.core.cache import cache
from .models import Joke, LandscapePhoto, ProductivityTip


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
    Get a random joke and save it to the database
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


def fetch_landscape_photos(page=1):
    """
    Fetch landscape photos from Unsplash API
    Returns: list of photo dictionaries or None if request fails
    """
    try:
        # Check if API key is configured
        if not hasattr(settings, 'UNSPLASH_API_KEY') or not settings.UNSPLASH_API_KEY:
            print("Unsplash API key not configured. Using default photos.")
            return get_default_photos()
        
        url = "https://api.unsplash.com/search/photos"
        headers = {
            'Authorization': f'Client-ID {settings.UNSPLASH_API_KEY}'
        }
        
        params = {
            'query': 'landscape nature scenery',
            'page': page,
            'per_page': 12,
            'orientation': 'landscape'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        photos = []
        for result in data.get('results', []):
            photo = {
                'id': result.get('id'),
                'title': result.get('alt_description', 'Landscape Photo'),
                'photographer': result.get('user', {}).get('name', 'Unknown'),
                'image_url': result.get('urls', {}).get('regular', ''),
                'thumbnail_url': result.get('urls', {}).get('small', ''),
                'location': result.get('user', {}).get('location', ''),
                'source_url': result.get('links', {}).get('html', ''),
            }
            photos.append(photo)
        
        return photos if photos else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching landscape photos: {e}")
        return get_default_photos()


def get_default_photos():
    """
    Return default landscape photos when API is not available
    """
    return [
        {
            'id': 'default1',
            'title': 'Mountain Landscape',
            'photographer': 'Nature Lover',
            'image_url': 'https://via.placeholder.com/1200x800?text=Mountain+Landscape',
            'thumbnail_url': 'https://via.placeholder.com/300x200?text=Mountain',
            'location': 'Alpine Region',
            'source_url': '#',
        },
        {
            'id': 'default2',
            'title': 'Ocean View',
            'photographer': 'Travel Photographer',
            'image_url': 'https://via.placeholder.com/1200x800?text=Ocean+View',
            'thumbnail_url': 'https://via.placeholder.com/300x200?text=Ocean',
            'location': 'Coastal Area',
            'source_url': '#',
        },
        {
            'id': 'default3',
            'title': 'Forest Path',
            'photographer': 'Outdoor Explorer',
            'image_url': 'https://via.placeholder.com/1200x800?text=Forest+Path',
            'thumbnail_url': 'https://via.placeholder.com/300x200?text=Forest',
            'location': 'Dense Forest',
            'source_url': '#',
        },
    ]


def get_random_landscape_photo():
    """
    Get a random landscape photo
    Returns: dict with photo data or None
    """
    cache_key = 'landscape_photos'
    photos = cache.get(cache_key)
    
    if not photos:
        photos = fetch_landscape_photos(page=random.randint(1, 5))
        if photos:
            cache.set(cache_key, photos, 3600)  # Cache for 1 hour
    
    if photos:
        photo = random.choice(photos)
        return photo
    
    return None


def get_random_productivity_tip():
    """
    Get a random productivity tip from database
    Returns: ProductivityTip object or None
    """
    tips_count = ProductivityTip.objects.count()
    
    if tips_count == 0:
        return None
    
    random_index = random.randint(0, tips_count - 1)
    return ProductivityTip.objects.all()[random_index]


def get_productivity_tips_by_category(category):
    """
    Get productivity tips by category
    Returns: QuerySet of ProductivityTip objects
    """
    return ProductivityTip.objects.filter(category=category)
