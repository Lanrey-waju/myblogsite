from blog.models import Post
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify


@receiver(pre_save, sender=Post)
def generate_slug(sender, instance, **kwargs):
    if not instance.publish:
        instance.publish = timezone.now()

    base_slug = slugify(instance.title)
    unique_slug = base_slug
    num = 1

    while Post.objects.filter(
        slug=unique_slug,
        publish__date=instance.publish.date(),
    ).exists():
        unique_slug = f"{base_slug}-{num}"
        num += 1
    instance.slug = unique_slug
