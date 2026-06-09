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
