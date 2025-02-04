from blog.models import Post
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField
from users.models import CustomUser


class PostSerializer(TaggitSerializer, ModelSerializer):

    # slug = serializers.SlugField(read_only=True)
    author = serializers.ReadOnlyField(source="author.first_name")
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "body",
            "author",
            "status",
            "created",
            "tags",
            "publish",
        ]
        read_only_fields = [
            "publish",
        ]

    def get_slug(self, obj):
        return obj.slug


class UserSerializer(ModelSerializer):
    blog_posts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Post.published.all()
    )

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "blog_posts", "date_joined"]
