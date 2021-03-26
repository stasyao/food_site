from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'text', 'image']

    def clean(self):
        """
        Контроль наличия и уникальности ингредиентов.
        Контроль того, что ингредиенты только из предложенного списка
        я реализовал в JS (см. dev_static/js/formRecipe.js)
        """
        super().clean()
        if (
            len(self.data.getlist('nameIngredient')) !=
            len(set(self.data.getlist('nameIngredient')))
        ):
            raise forms.ValidationError(
                'Пожалуйста, уберите повторяющиеся ингредиенты'
            )
        if 'nameIngredient' not in self.data:
            raise forms.ValidationError(
                'Нужно добавить минимум один ингридиент'
            )
