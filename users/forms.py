from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from django.contrib.auth import get_user_model

# Deine User Creation Forms 
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email',)