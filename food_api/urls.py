from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


urlpatterns = [
    path('ingredients/', views.IngredientListView.as_view({'get': 'list'})),
    path('follow/', views.FollowingAdd.as_view()),
    path('follow/<int:id>', views.FollowingDelete.as_view()),
    path('favorites/', views.SelectFavoriteRecipeView.as_view()),
    path('favorites/<int:pk>', views.DeleteFavoriteView.as_view(),
         name="favorite-delete",),
    path('purchases/', views.PurchaseAdd.as_view()),
    path('purchases/<int:id>', views.PurchaseDelete.as_view()),
]
