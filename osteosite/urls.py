from django.contrib import admin
from django.urls import path
from predictor import views   # ✅ import your views file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # ✅ this connects homepage
]
