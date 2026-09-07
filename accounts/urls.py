from django.urls import path
from .views import register
from .views import user_login
from .views import logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
]