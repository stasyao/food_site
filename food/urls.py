from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'food'

handler403 = 'food.views.permission_denied'
handler404 = 'food.views.page_not_found'
handler500 = 'food.views.server_error'


urlpatterns = [
     path('', views.RecipeListView.as_view(), name='home'),
     # "избранное" авторизованного юзера
     path('selected/<int:pk>', views.RecipeListView.as_view(),
          name='selected_food'),
     # рецепты конкретного автора
     path('author_page/<int:pk>', views.RecipeListView.as_view(),
          name='food_author_page'),
     # подписки авторизованного юзера
     path('subscriptions/', views.SubscriptionsListView.as_view(),
          name='subscriptions'),
     # посмотреть список покупок и удалить из него записи
     path('purchaces_list/<int:pk>', views.PurchasesView.as_view(),
          name='user_purchases'),
     # скачать список покупок
     path('get_foodlist/', views.DownloadPurchases.as_view(),
          name='get_foodlist'),
     # редактировать рецепт
     path('edit/<int:pk>', views.RecipeCreateUpdateView.as_view(),
          name='food_edit'),
     # создать рецепт
     path('create', views.RecipeCreateUpdateView.as_view(),
          name='food_create'),
     # удалить рецепт
     path('delete/<int:pk>', views.RecipeDeleteView.as_view(),
          name='food_delete'),
     # посмотреть страницу с конкретным рецептом
     path('<int:pk>/', views.RecipeView.as_view(), name='food'),
     # страница об авторе
     path('about/', TemplateView.as_view(template_name='about.html'),
          name='about'),
     # страница об используемых технологиях
     path('spec/', TemplateView.as_view(template_name='spec.html'),
          name='spec'),
     path('site_info/', TemplateView.as_view(template_name='site_info.html'),
          name='site_info'),
]
