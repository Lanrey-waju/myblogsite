from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.urls import reverse

User = get_user_model()
# Create your tests here.
class BlogTests(TestCase):

    def setUp(self):
        pass