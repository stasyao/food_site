from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from food.models import Follow, Ingredient, Purchase, Recipe, SelectedRecipe

from .serializer import (FollowersSerializer, IngredientSerializer,
                         PurchaseSerializer, SelectedRecipiesSerializer)


class CustomCreateMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class IngredientListView(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]


class SelectFavoriteRecipeView(CreateAPIView, CustomCreateMixin):
    queryset = SelectedRecipe.objects.all()
    serializer_class = SelectedRecipiesSerializer


class DeleteFavoriteView(APIView):
    def delete(self, request, pk):
        selected = get_object_or_404(
            SelectedRecipe,
            user=request.user,
            recipe=pk
        )
        selected.delete()
        return Response({"success": True})


class PurchaseAdd(CreateAPIView, CustomCreateMixin):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class PurchaseDelete(APIView):
    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        purchase = recipe.purchases.filter(user=request.user)
        if purchase.delete():
            return Response({"success": True})
        return Response({"success": False})


class FollowingAdd(CreateAPIView, CustomCreateMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowersSerializer


class FollowingDelete(APIView):
    def delete(self, request, id):
        author = get_object_or_404(get_user_model(), id=id)
        subscribe = author.following.filter(user=request.user)
        if subscribe.delete():
            return Response({"success": True})
        return Response({"success": False})
