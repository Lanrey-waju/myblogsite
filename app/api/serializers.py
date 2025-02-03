from blog.models import Post
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TaggitSerializer, TagListSerializerField


class PostSerializer(TaggitSerializer, ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ["id", "title", "body", "created", "tags", "publish"]
