from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'source')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
