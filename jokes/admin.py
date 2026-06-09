from django.contrib import admin
from .models import Joke


@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ('setup', 'punchline', 'joke_type', 'created_at')
    list_filter = ('joke_type', 'created_at')
    search_fields = ('setup', 'punchline')
    readonly_fields = ('created_at',)
