from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    BREAKFAST = 'завтрак'
    LUNCH = 'обед'
    DINNER = 'ужин'
    MEAL_CHOICES = ((BREAKFAST, 'завтрак'), (LUNCH, 'обед'), (DINNER, 'ужин'),)
    ORANGE = 'orange'
    GREEN = 'green'
    PURPLE = 'purple'
    COLOR_CHOICES = ((ORANGE, 'оранжевый'), (GREEN, 'зеленый'),
                     (PURPLE, 'фиолетовый'),)

    title = models.CharField('название', max_length=20, unique=True,
                             choices=MEAL_CHOICES, default=BREAKFAST)
    slug = models.SlugField(null=True)
    color = models.CharField('цвет', max_length=20, unique=True,
                             choices=COLOR_CHOICES, default=GREEN)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('название ингредиента', max_length=100,)
    dimension = models.CharField('eдиница измерения', max_length=20,
                                 default='шт.',)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.title


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


class Recipe(models.Model):
    title = models.CharField('Название', max_length=100,)
    tags = models.ManyToManyField(to=Tag, verbose_name='теги')
    image = models.ImageField('фото', upload_to='image/',
                              default='image/default.jpg')
    text = models.TextField(verbose_name='описание')
    cooking_time = models.PositiveIntegerField('время приготовления, мин',)
    pub_date = models.DateTimeField('дата публикации рецпета',
                                    auto_now_add=True, db_index=True,)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='автор')
    ingredients = models.ManyToManyField(to=Ingredient,
                                         through='RecipeIngredientAmount',
                                         verbose_name='ингредиенты',)
    objects = RecipeManager()

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('food:food', kwargs={'pk': self.pk})


class RecipeIngredientAmount(models.Model):
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField('количество')

    class Meta:
        verbose_name = 'ингридиент рецепта'
        verbose_name_plural = 'ингридиенты рецепта'


class Purchase(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE,
                             related_name='purchases',
                             verbose_name='пользователь',)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE,
                               related_name='purchases',
                               verbose_name='рецепт',)

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в покупки {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(to=get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='подписчик',)

    author = models.ForeignKey(to=get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='автор',)

    class Meta:
        ordering = ('author',)
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class SelectedRecipies(models.Model):
    user = models.ForeignKey(to=get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='selected',
                             verbose_name='пользователь',)

    recipe = models.ForeignKey(to=Recipe,
                               on_delete=models.CASCADE,
                               related_name='selected',
                               verbose_name='рецепт',)

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избраные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_selected_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'
