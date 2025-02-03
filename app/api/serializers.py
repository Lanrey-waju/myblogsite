from blog.models import Post
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField
from users.models import CustomUser


class PostSerializer(TaggitSerializer, ModelSerializer):

    author = serializers.ReadOnlyField(source="author.email")
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ["id", "title", "body", "author", "created", "tags", "publish"]


class UserSerializer(ModelSerializer):
    blog_posts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Post.published.all()
    )

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "blog_posts", "date_joined"]
