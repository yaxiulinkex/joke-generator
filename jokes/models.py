from django.db import models


class Joke(models.Model):
    """Model to store joke history"""
    setup = models.TextField()
    punchline = models.TextField()
    joke_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Jokes'

    def __str__(self):
        return f"{self.setup} - {self.punchline}"


class GameScore(models.Model):
    """Model to store game scores"""
    GAME_CHOICES = [
        ('tictactoe', 'Tic Tac Toe'),
        ('guessnum', 'Guess the Number'),
        ('memory', 'Memory Game'),
    ]
    
    game_type = models.CharField(max_length=20, choices=GAME_CHOICES)
    score = models.IntegerField()
    player_name = models.CharField(max_length=100, default='Anonymous')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at']
        verbose_name_plural = 'Game Scores'

    def __str__(self):
        return f"{self.player_name} - {self.get_game_type_display()}: {self.score}"


class LandscapePhoto(models.Model):
    """Model to store landscape photos"""
    title = models.CharField(max_length=200)
    photographer = models.CharField(max_length=100)
    image_url = models.URLField()
    thumbnail_url = models.URLField()
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Landscape Photos'

    def __str__(self):
        return self.title


class ProductivityTip(models.Model):
    """Model to store productivity tips"""
    CATEGORY_CHOICES = [
        ('productivity', 'Productivity'),
        ('wellness', 'Wellness'),
        ('mindfulness', 'Mindfulness'),
        ('health', 'Health'),
        ('focus', 'Focus'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    duration_minutes = models.IntegerField(default=5, help_text="Suggested duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Productivity Tips'

    def __str__(self):
        return self.title
