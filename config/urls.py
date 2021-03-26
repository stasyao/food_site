import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import settings

urlpatterns = [
    # админка
    path('admin/', admin.site.urls),
    # апи для добавления/удаления через JS подписок, покупок, избранного
    # а также поиска ингредиентов при создании/редактировании рецепта
    path('api/', include('food_api.urls')),
    # маршруты для аутентификации/авторизации
    path('auth/', include("users.urls")),
    # маршруты для CRUD рецептов
    path('', include('food.urls')),
    # настройка для джанго-тулбара
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
