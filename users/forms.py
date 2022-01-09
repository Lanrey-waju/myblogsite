from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from .models import CustomUser

# Deine User Creation Forms 
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)