from django.shortcuts import render
from django.http import JsonResponse
from .models import Joke
from .services import get_random_joke, get_random_joke_by_type


def index(request):
    """Main page with random joke generator"""
    joke = None
    error = None
    
    if request.method == 'POST':
        joke = get_random_joke()
        if not joke:
            error = "Sorry, couldn't fetch a joke. Please try again."
    
    return render(request, 'jokes/index.html', {'joke': joke, 'error': error})


def joke_by_type(request, joke_type):
    """Get a joke by specific type"""
    valid_types = ['general', 'knock-knock', 'programming']
    
    if joke_type not in valid_types:
        error = f"Invalid joke type. Choose from: {', '.join(valid_types)}"
        return render(request, 'jokes/index.html', {'error': error})
    
    joke = get_random_joke_by_type(joke_type)
    
    if not joke:
        error = f"Couldn't fetch a {joke_type} joke. Please try again."
        return render(request, 'jokes/index.html', {'error': error})
    
    return render(request, 'jokes/index.html', {'joke': joke})


def joke_history(request):
    """Display joke history"""
    jokes = Joke.objects.all()[:20]  # Get last 20 jokes
    return render(request, 'jokes/history.html', {'jokes': jokes})


def get_random_joke_api(request):
    """API endpoint to get random joke as JSON"""
    joke = get_random_joke()
    
    if joke:
        return JsonResponse(joke)
    else:
        return JsonResponse({'error': 'Failed to fetch joke'}, status=500)
