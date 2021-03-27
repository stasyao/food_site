from django.db import models


class RecipeManager(models.Manager):
    def get_info_for_subscription_page(self):
        total_recipes = self.count()
        if total_recipes > 3:
            rest = total_recipes - 3
            if rest == 11 or rest % 10 > 4:
                word = 'рецептов'
            elif rest % 10 == 1:
                word = 'рецепт'
            elif rest % 10 <= 4:
                word = 'рецепта'
        else:
            rest = 0
            word = None
        return {
            'recipies': self.all()[:3],
            'rest': rest,
            'word': word,
        }
