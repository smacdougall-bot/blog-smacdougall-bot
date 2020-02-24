from django.contrib import admin
from . import models
# Register your models here.

# The Post models
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'text',
        'approved',
        'created',
        'updated',
    )

    search_fields = (
        'name',
        'email',
        'text',
    )

    list_filter = (
        'approved',
    )

class CommentInline(admin.StackedInline):
    model = models.Comment
    fields = ('name', 'email', 'text', 'approved')
    readonly_fields = ('name', 'email', 'text')
    extra = 0
    max_num = 0
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
        'author',
        'status',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )

    inlines = [
        CommentInline,
    ]

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Post, PostAdmin)
