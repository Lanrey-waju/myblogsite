import uuid
from django.db import models
from django.db.models.fields import related
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

CustomUser = get_user_model()
now = timezone.now
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        """Returns published posts when queried"""
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=now)
    created = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args={self.publish.year, self.publish.month, self.publish.day, self.slug})
    
    
