from django.contrib import admin

from .models import Comment, Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "publish",
        "status",
    )
    list_filter = (
        "status",
        "created_at",
        "publish",
        "author",
    )
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
    search_fields = ("title", "body")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "post",
        "created_at",
        "active",
    )
    list_filter = (
        "active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "email",
        "body",
    )
