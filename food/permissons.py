from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import Recipe


class CustomPermissions(UserPassesTestMixin):
    """
    Пермишены для доступа только к своему "Избранному", "Списку покупок",
    редактированию и удалению только своего рецепта.
    """
    def test_func(self):
        current_url = self.request.resolver_match.view_name
        own_user_pages = [
            'food:selected_food',
            'food:user_purchases',
        ]
        own_recipies_pages = [
            'food:food_edit',
            'food:food_delete'
        ]
        user_or_recipe_id = self.kwargs.get('pk')
        if user_or_recipe_id and current_url in own_user_pages:
            author = get_object_or_404(get_user_model(), pk=user_or_recipe_id)
            return (
                self.request.user.is_authenticated and
                self.request.user == author
            )
        if user_or_recipe_id and current_url in own_recipies_pages:
            recipe = get_object_or_404(Recipe, pk=user_or_recipe_id)
            return (
                self.request.user.is_authenticated and
                self.request.user == recipe.author
            )
        return True
