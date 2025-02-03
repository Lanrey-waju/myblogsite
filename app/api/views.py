from blog.models import Post
from rest_framework import generics
from users.models import CustomUser

from .serializers import PostSerializer, UserSerializer


# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
