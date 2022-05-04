from debug_toolbar import APP_NAME
from django.urls import path

from .views import signup

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
]
