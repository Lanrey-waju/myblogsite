from django import forms

from .models import Comment, Post


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            "name",
            "email",
            "body",
        )


class ContactMeForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    message = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Search"})
    )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            "title",
            "body",
        )
