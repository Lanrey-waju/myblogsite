from blog.models import Post
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField
from users.models import CustomUser


class CustomTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        # Split input into individual tags, whether it's a string or list
        if isinstance(value, str):
            tags = [tag.strip() for tag in value.split(",") if tag.strip()]

        elif isinstance(value, list):
            tags = []
            for item in value:
                if isinstance(item, str):
                    tags.extend([tag.strip() for tag in item.split(",") if tag.strip()])
                else:
                    tags.append(str(item).strip())
        else:
            tags = [str(value).strip()]

        return super().to_internal_value(tags)


class PostSerializer(TaggitSerializer, HyperlinkedModelSerializer):

    # slug = serializers.SlugField(read_only=True)
    author = serializers.ReadOnlyField(source="author.first_name")
    tags = CustomTagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "title",
            "slug",
            "body",
            "author",
            "status",
            "created_at",
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
        fields = ["id", "email", "first_name", "last_name", "blog_posts", "date_joined"]
