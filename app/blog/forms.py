from django import forms
from .models import Comments, Post

class CommentsForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ("name", "email", "body",)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    to = forms.EmailField(required=False)
    comments = forms.CharField(required=False, widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search'}))

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "body",)