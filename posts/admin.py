from django.contrib import admin
from .models import Post, Category, Tag, Comment, Contact, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_approved", "created_time")
    inlines = [CommentInline]
    list_filter = ["is_approved"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "created_time"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "created_time"]


class ContactAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    search_fields = ["created_time", "is_answered", "answer_time"]
    list_filter = ["is_answered", "created_time"]
    inlines = [AnswerInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Contact, ContactAdmin)
