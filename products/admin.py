from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Offer, Tag


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1
	fields = ('image', 'alt_text', 'is_main', 'order')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'image_preview', 'created_at')
	prepopulated_fields = {'slug': ('name',)}
	readonly_fields = ('image_preview',)

	def image_preview(self, obj):
		if obj and obj.image:
			return format_html('<img src="{}" style="max-height:50px; border-radius: 50%;"/>', obj.image.url)
		return '(no image)'
	image_preview.short_description = 'Icon Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'discount_percentage', 'is_active', 'availability')
	list_filter = ('category', 'is_active')
	search_fields = ('name', 'short_description', 'tags__name')
	prepopulated_fields = {'slug': ('name',)}
	inlines = [ProductImageInline]
	filter_horizontal = ('tags',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ('product', 'is_main', 'order')
	list_filter = ('is_main',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
	list_display = ('title', 'offer_type', 'discount_type', 'discount_value', 'priority', 'active', 'start_date', 'end_date')
	list_filter = ('active', 'offer_type', 'discount_type')
	search_fields = ('title', 'subtitle', 'description')
	filter_horizontal = ('products', 'categories')
	readonly_fields = ('preview',)

	fieldsets = (
		('Identity / Marketing', {
			'fields': ('title', 'subtitle', 'badge_text', 'image', 'preview', 'description')
		}),
		('Logic / Discount', {
			'fields': ('offer_type', 'discount_type', 'discount_value', 'max_discount', 'min_cart_value', 'stackable', 'priority')
		}),
		('Targeting', {
			'fields': ('products', 'categories', 'user_eligibility')
		}),
		('Validity / Usage', {
			'fields': ('start_date', 'end_date', 'active', 'usage_limit_per_user', 'total_usage_limit', 'times_used')
		}),
	)

	def preview(self, obj):
		if obj and obj.image:
			return format_html('<img src="{}" style="max-height:120px;"/>', obj.image.url)
		return '(no image)'
	preview.short_description = 'Banner preview'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'created_at')
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}
