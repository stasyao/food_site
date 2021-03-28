from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView

from .forms import RecipeForm
from .models import Ingredient, Recipe
from .models import RecipeIngredientAmount as IngAmount
from .models import Tag
from .permissons import CustomPermissions


class RecipeListView(CustomPermissions, ListView):
    """
    Отобразить страницы "Главная", "Избранное", "Страница автора"
    """
    context_object_name = 'food_list'
    paginate_by = 3
    template_name = 'food/index.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.selected_food_url = (request.resolver_match.view_name ==
                                  'food:selected_food')
        self.author_page = (request.resolver_match.view_name ==
                            'food:food_author_page')
        self.auth_user = request.user.is_authenticated

    def get_queryset(self):
        """
        Выбор кверисета в зависимости от вызываемого урла и проставленных тегов.
        """
        if self.selected_food_url:
            qs = Recipe.objects.filter(
                pk__in=self.request.user.selected.values_list('recipe',
                                                              flat=True)
                )
        elif self.author_page:
            qs = Recipe.objects.filter(author=self.kwargs['pk'])
        else:
            qs = Recipe.objects.all()
        if self.request.GET.getlist('tag'):
            tags = self.request.GET.getlist('tag')
            qs = qs.filter(tags__slug__in=tags).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'tags': Tag.objects.all()})
        if self.auth_user:
            selected_recipies = self.request.user.selected.values_list(
                'recipe', flat=True
            )
            purchases_list = self.request.user.purchases.values_list(
                'recipe', flat=True
            )
            context.update(
                {'selected_recipies': selected_recipies,
                 'purchases_list': purchases_list}
            )
        can_be_follower = (self.author_page and self.auth_user and
                           self.request.user.pk != self.kwargs['pk'])
        if can_be_follower:
            is_follower = self.request.user.follower.filter(
                author=self.kwargs['pk']
            ).exists()
            context.update(
                {'can_be_follower': can_be_follower,
                 'is_follower': is_follower,
                 'author_recipe': get_object_or_404(
                     get_user_model(), pk=self.kwargs['pk']
                     )}
            )
        return context

    def paginate_queryset(self, queryset, page_size):
        """
        Переопределяем поведение пагинатора в нештатных ситуациях.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        p_kwarg = self.page_kwarg
        page = self.kwargs.get(p_kwarg) or self.request.GET.get(p_kwarg) or 1
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return (paginator, page, page.object_list, page.has_other_pages())


class PurchasesView(LoginRequiredMixin, ListView):
    context_object_name = 'purchases_list'
    paginate_by = 10
    template_name = 'food/purchases_list.html'

    def get_queryset(self):
        user = self.request.user
        qs = Recipe.objects.filter(
            id__in=user.purchases.values_list('recipe', flat=True)
        )
        return qs


class RecipeView(DetailView):
    """
    Просмотр страницы с конкретным рецептом.
    """
    context_object_name = 'recipe'
    queryset = Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            is_follower = self.request.user.follower.filter(
                author=self.object.author
            ).exists()
            has_added_recipe = self.request.user.purchases.filter(
                recipe=self.object
            ).exists()
            has_selected = self.request.user.selected.filter(
                recipe=self.object
            ).exists()
            context.update(
                {'is_follower': is_follower,
                 'has_added_recipe': has_added_recipe,
                 'has_selected': has_selected}
            )
        return context


class RecipeCreateUpdateView(LoginRequiredMixin, CustomPermissions, UpdateView):
    """
    Создание и редактирование рецептов.
    """
    model = Recipe
    form_class = RecipeForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            self.ingredients = self.object.recipeingredientamount_set.all()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.object:
            if 'current_items' not in ctx:
                self.ingredients = self.object.recipeingredientamount_set.all()
                ctx['current_items'] = self.ingredients.values(
                    'ingredient__title', 'amount', 'ingredient__dimension'
                )
        return ctx

    def form_invalid(self, form):
        """
        Оставить выбранные с фронта ингредиенты после перезагрузки формы.
        """
        form_data = form.data.copy()
        items = zip(
                form_data.getlist('nameIngredient'),
                form_data.getlist('valueIngredient'),
                form_data.getlist('dimensionIngredient'),
        )
        current_items = [
            {'ingredient__title': item[0], 'amount': item[1],
             'ingredient__dimension': item[2]}
            for item in items
        ]
        return self.render_to_response(
            self.get_context_data(form=form, current_items=current_items)
        )

    def form_valid(self, form):
        selected_ingredients = form.data.getlist('nameIngredient')
        selected_amount = form.data.getlist('valueIngredient')
        if not self.object:
            form.instance.author = self.request.user
            self.object = form.save()
        else:
            self.object = form.save()
            if (
                list(map(lambda x: (x.ingredient.title, str(x.amount)),
                     self.object.recipeingredientamount_set.all())) !=
                list(zip(*[selected_ingredients, selected_amount]))
                    ):
                # если изменения были, зачищаем "старые" ингредиенты
                self.object.ingredients.clear()
            # если изменений не было, базу не дергаем
            else:
                return super().form_valid(form)
        selected_ingredients = map(lambda x: Ingredient.objects.get(title=x),
                                   selected_ingredients)
        ingredients_for_recipe = [
            IngAmount(
                ingredient=ing,
                recipe=self.object,
                amount=amount
            )
            for ing, amount in zip(selected_ingredients, selected_amount)
        ]
        IngAmount.objects.bulk_create(ingredients_for_recipe)
        return super().form_valid(form)


class RecipeDeleteView(CustomPermissions, DeleteView):
    """
    Удалить конкретный рецепт.
    """
    model = Recipe
    success_url = reverse_lazy('food:home')


class DownloadPurchases(LoginRequiredMixin, View):
    """
    Посчитать количество каждого ингредиента в отобранных в покупки
    рецептах и вывести пользователю txt-список.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user = request.user
        ingredients_for_purchase = IngAmount.objects.filter(
                recipe__in=user.purchases.values_list('recipe', flat=True)
            ).values(
                'ingredient__title', 'ingredient__dimension'
            ).annotate(qty=Sum('amount'))
        food_list = map(
            lambda x: (
                f'{x["ingredient__title"]}-'
                f'{x["qty"]} {x["ingredient__dimension"]}\n'
            ),
            ingredients_for_purchase
        )
        filename = 'food_list.txt'
        response = HttpResponse(food_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class SubscriptionsListView(LoginRequiredMixin, ListView):
    template_name = 'food/following.html'
    context_object_name = 'authors'

    def get_queryset(self):
        user = self.request.user
        authors = get_user_model().objects.filter(
            pk__in=user.follower.values_list('author', flat=True)
        )
        return authors
