from django.contrib import admin
from django.utils.html import format_html
from .models import Banner, FeedType


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slot', 'is_active', 'order', 'created_at', 'image_preview')
    list_filter = ('slot', 'is_active')
    search_fields = ('title', 'alt_text')
    readonly_fields = ('image_preview',)
    ordering = ('order',)

    def image_preview(self, obj):
        if not obj.image:
            return '(no image)'
        return format_html('<img src="{}" style="max-height:70px;"/>', obj.image.url)

    image_preview.short_description = 'Preview'


@admin.register(FeedType)
class FeedTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'protein_content', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if not obj.image:
            return '(no image)'
        return format_html('<img src="{}" style="max-height:70px;"/>', obj.image.url)
    
    image_preview.short_description = 'Preview'
