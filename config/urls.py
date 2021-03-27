import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import settings

handler403 = 'config.views.permission_denied'
handler404 = 'config.views.page_not_found'
handler500 = 'config.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('food_api.urls')),
    path('auth/', include('users.urls')),
    path('', include('food.urls')),
    # настройка для джанго-тулбара
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
