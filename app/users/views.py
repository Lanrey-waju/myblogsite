from django.shortcuts import render
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    #instantiate user creation form
    form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})