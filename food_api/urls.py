from django.urls import include, path

urlpatterns = [
    path('v1/', include('food_api.v1.urls')),
]
