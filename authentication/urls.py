# authentication/urls.py

from django.urls import path
from .views import login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('login', login, name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
