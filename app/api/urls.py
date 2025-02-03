from api import views
from django.urls import path

urlpatterns = [
    # posts endpoints
    path("posts/", views.PostList.as_view()),
    path("posts/<uuid:pk>/", views.PostDetail.as_view()),
    # users endpoints
    path("users/", views.UserList.as_view()),
]
