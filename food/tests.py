"""
Тесты в процессе подготовки
"""
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse


class TestHomePage(TestCase):
    # Тестируемые маршруты
    URL_HOME_PAGE = reverse("food:home")

    def setUp(self):
        cache.clear()

    def test_home_page_status_code(self):
        """
        Проверить, загружается ли главная страница.
        """
        response = self.client.get(self.URL_HOME_PAGE)
        self.assertEqual(response.status_code, 200)
