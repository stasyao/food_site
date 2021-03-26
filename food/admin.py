from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredientAmount, Tag


class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredientAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        'title',
        'cooking_time',
        'text',
        'author',
        'pub_date',
    )
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientAmountInline,)
    list_filter = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'color')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'dimension')
    empty_value_display = '-пусто-'
    list_filter = ('title',)
