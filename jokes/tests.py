from django.test import TestCase
from django.urls import reverse
from .models import Joke


class JokeModelTests(TestCase):
    def setUp(self):
        self.joke = Joke.objects.create(
            setup="Why did the programmer quit?",
            punchline="Because he didn't get arrays.",
            joke_type="programming"
        )

    def test_joke_creation(self):
        self.assertEqual(self.joke.setup, "Why did the programmer quit?")
        self.assertEqual(self.joke.joke_type, "programming")

    def test_joke_string_representation(self):
        expected = f"{self.joke.setup} - {self.joke.punchline}"
        self.assertEqual(str(self.joke), expected)


class JokeViewTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('jokes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jokes/index.html')

    def test_history_page_loads(self):
        response = self.client.get(reverse('jokes:history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jokes/history.html')

    def test_invalid_joke_type(self):
        response = self.client.get(reverse('jokes:by_type', args=['invalid']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid joke type')
