from ckeditor_uploader.fields import RichTextUploadingField
from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

CustomUser = get_user_model()
now = timezone.now
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        """Returns published posts when queried"""
        return super(PublishedManager, self).get_queryset().filter(status="published")


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(
    #     Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE
    # )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Post(TimeStampedModel):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date="publish",
        blank=True,
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    tags = TaggableManager(through=UUIDTaggedItem)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    body = RichTextUploadingField()
    email = models.EmailField(max_length=254)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
