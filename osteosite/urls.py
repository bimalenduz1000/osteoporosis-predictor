from django.contrib import admin
from django.urls import path
from predictor import views   # 👈 ei line ta add korbo — jate amra views.py er function use korte pari

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # 👈 eta holo amader main page URL
]
