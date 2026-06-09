from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Max
from .models import Joke, GameScore, LandscapePhoto, ProductivityTip
from .services import (
    get_random_joke, 
    get_random_joke_by_type,
    get_random_landscape_photo,
    get_random_productivity_tip,
    get_productivity_tips_by_category
)


def dashboard(request):
    """Main dashboard with all sections"""
    context = {
        'page': 'dashboard',
        'joke_count': Joke.objects.count(),
        'game_count': GameScore.objects.count(),
        'top_scores': GameScore.objects.values('game_type').annotate(
            best_score=Max('score')
        ).order_by('-best_score'),
        'leaderboard': GameScore.objects.all().order_by('-score')[:5],
        'tip': get_random_productivity_tip(),
    }
    return render(request, 'jokes/dashboard.html', context)


# ==================== JOKES SECTION ====================
def index(request):
    """Main page with random joke generator"""
    joke = None
    error = None
    
    if request.method == 'POST':
        joke = get_random_joke()
        if not joke:
            error = "Sorry, couldn't fetch a joke. Please try again."
    
    return render(request, 'jokes/index.html', {'joke': joke, 'error': error, 'page': 'jokes'})


def joke_by_type(request, joke_type):
    """Get a joke by specific type"""
    valid_types = ['general', 'knock-knock', 'programming']
    
    if joke_type not in valid_types:
        error = f"Invalid joke type. Choose from: {', '.join(valid_types)}"
        return render(request, 'jokes/index.html', {'error': error, 'page': 'jokes'})
    
    joke = get_random_joke_by_type(joke_type)
    
    if not joke:
        error = f"Couldn't fetch a {joke_type} joke. Please try again."
        return render(request, 'jokes/index.html', {'error': error, 'page': 'jokes'})
    
    return render(request, 'jokes/index.html', {'joke': joke, 'page': 'jokes'})


def joke_history(request):
    """Display joke history"""
    jokes = Joke.objects.all()[:50]
    return render(request, 'jokes/history.html', {'jokes': jokes, 'page': 'jokes'})


@require_http_methods(["GET"])
def get_random_joke_api(request):
    """API endpoint to get random joke as JSON"""
    joke = get_random_joke()
    
    if joke:
        return JsonResponse(joke)
    else:
        return JsonResponse({'error': 'Failed to fetch joke'}, status=500)


# ==================== GAMES SECTION ====================
def games(request):
    """Games hub page"""
    games_list = [
        {'id': 'tictactoe', 'name': 'Tic Tac Toe', 'icon': '🎯', 'description': 'Classic strategy game'},
        {'id': 'guessnum', 'name': 'Guess the Number', 'icon': '🎲', 'description': 'Quick number guessing'},
        {'id': 'memory', 'name': 'Memory Game', 'icon': '🧠', 'description': 'Test your memory'},
    ]
    
    top_scores = {}
    for game in games_list:
        score = GameScore.objects.filter(game_type=game['id']).order_by('-score').first()
        if score:
            top_scores[game['id']] = score
    
    context = {
        'page': 'games',
        'games': games_list,
        'top_scores': top_scores,
    }
    return render(request, 'jokes/games.html', context)


@require_http_methods(["GET"])
def game_detail(request, game_id):
    """Display specific game"""
    games_map = {
        'tictactoe': 'Tic Tac Toe',
        'guessnum': 'Guess the Number',
        'memory': 'Memory Game',
    }
    
    if game_id not in games_map:
        return redirect('jokes:games')
    
    leaderboard = GameScore.objects.filter(game_type=game_id).order_by('-score')[:10]
    
    context = {
        'page': 'games',
        'game_id': game_id,
        'game_name': games_map[game_id],
        'leaderboard': leaderboard,
    }
    return render(request, f'jokes/game_{game_id}.html', context)


@require_http_methods(["POST"])
def save_game_score(request):
    """Save game score"""
    try:
        game_type = request.POST.get('game_type')
        score = int(request.POST.get('score', 0))
        player_name = request.POST.get('player_name', 'Anonymous')
        
        if game_type not in ['tictactoe', 'guessnum', 'memory']:
            return JsonResponse({'error': 'Invalid game type'}, status=400)
        
        game_score = GameScore.objects.create(
            game_type=game_type,
            score=score,
            player_name=player_name
        )
        
        # Count how many have higher or equal score (rank)
        rank = GameScore.objects.filter(
            game_type=game_type,
            score__gt=score
        ).count() + 1
        
        return JsonResponse({
            'success': True,
            'message': f'Score saved! {player_name}: {score}',
            'rank': rank
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def game_leaderboard(request):
    """Display game leaderboard"""
    game_type = request.GET.get('type', 'tictactoe')
    leaderboard = GameScore.objects.filter(game_type=game_type).order_by('-score')[:50]
    
    games_map = {
        'tictactoe': 'Tic Tac Toe',
        'guessnum': 'Guess the Number',
        'memory': 'Memory Game',
    }
    
    context = {
        'page': 'games',
        'game_type': game_type,
        'game_name': games_map.get(game_type, 'Unknown'),
        'leaderboard': leaderboard,
    }
    return render(request, 'jokes/leaderboard.html', context)


# ==================== PHOTOS SECTION ====================
def photos(request):
    """Landscape photos gallery"""
    context = {
        'page': 'photos',
    }
    return render(request, 'jokes/photos.html', context)


@require_http_methods(["GET"])
def get_random_photo_api(request):
    """API endpoint to get random photo"""
    photo = get_random_landscape_photo()
    
    if photo:
        return JsonResponse(photo)
    else:
        return JsonResponse({'error': 'Failed to fetch photo'}, status=500)


# ==================== PRODUCTIVITY TIPS SECTION ====================
def productivity_hub(request):
    """Productivity and wellness hub"""
    category = request.GET.get('category', '')
    
    if category:
        tips = get_productivity_tips_by_category(category)
    else:
        tips = ProductivityTip.objects.all()[:20]
    
    categories = ProductivityTip.CATEGORY_CHOICES
    
    context = {
        'page': 'productivity',
        'tips': tips,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'jokes/productivity.html', context)


@require_http_methods(["GET"])
def get_random_tip_api(request):
    """API endpoint to get random productivity tip"""
    tip = get_random_productivity_tip()
    
    if tip:
        return JsonResponse({
            'id': tip.id,
            'title': tip.title,
            'content': tip.content,
            'category': tip.category,
            'duration_minutes': tip.duration_minutes,
        })
    else:
        return JsonResponse({'error': 'No tips available'}, status=500)
