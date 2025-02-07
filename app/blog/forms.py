import os

import requests
from django import forms
from django.conf import settings
from django.core.mail import send_mail

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
    title = forms.CharField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    message = forms.CharField(required=False, widget=forms.Textarea)
    captcha = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("title"):
            raise forms.ValidationError("Likely bot submission detected")

        recaptcha_response = cleaned_data.get("captcha")
        data = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data)
        if not r.json().get("success"):
            raise forms.ValidationError("invalid reCAPTCHA")

    def send_email(self):
        subject = "Blog Inquiry"
        message = self.cleaned_data.get("message")
        from_email = self.cleaned_data.get("email")
        print(subject, message, from_email)

        send_mail(
            subject, message, from_email, [os.environ.get("EMAIL")], fail_silently=False
        )


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
