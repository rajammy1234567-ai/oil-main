from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, storage=MediaCloudinaryStorage())
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.CharField(max_length=512, blank=True)
    long_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    how_to_use = models.TextField(blank=True)
    details = models.JSONField(blank=True, null=True)
    additional_details = models.TextField(blank=True)

    # GENDER_MALE = 'male'
    # GENDER_FEMALE = 'female'
    # GENDER_UNISEX = 'unisex'
    # GENDER_CHOICES = [
    #     (GENDER_MALE, 'Male'),
    #     (GENDER_FEMALE, 'Female'),
    #     (GENDER_UNISEX, 'Unisex'),
    # ]
    # gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_UNISEX)

    AVAIL_AVAILABLE = 'available'
    AVAIL_OUT = 'out_of_stock'
    AVAILABILITY_CHOICES = [
        (AVAIL_AVAILABLE, 'Available'),
        (AVAIL_OUT, 'Out of stock'),
    ]
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default=AVAIL_AVAILABLE)

    social_facebook = models.URLField(max_length=500, blank=True, null=True)
    social_instagram = models.URLField(max_length=500, blank=True, null=True)
    social_x = models.URLField(max_length=500, blank=True, null=True)
    social_youtube = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Tags for search and filtering
    tags = models.ManyToManyField('Tag', related_name='products', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # make a unique slug
            base = slugify(self.name)
            slug = base
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first()
        if img:
            return img.image.url
        img = self.images.first()
        return img.image.url if img else ''


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # ensure uniqueness
            base = self.slug
            i = 1
            while Tag.objects.filter(slug=self.slug).exclude(pk=getattr(self, 'pk', None)).exists():
                self.slug = f"{base}-{i}"
                i += 1
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', storage=MediaCloudinaryStorage())
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False, help_text='Show this image on product cards')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product_id} ({self.pk})"


class Offer(models.Model):
    # Marketing / identity
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='offers/', blank=True, null=True, storage=MediaCloudinaryStorage())
    badge_text = models.CharField(max_length=50, blank=True, help_text='Short label shown on product cards')

    # Offer types
    TYPE_PRODUCT = 'product'
    TYPE_CATEGORY = 'category'
    TYPE_CART = 'cart'
    TYPE_NEW_USER = 'new_user'
    OFFER_TYPE_CHOICES = [
        (TYPE_PRODUCT, 'Product'),
        (TYPE_CATEGORY, 'Category'),
        (TYPE_CART, 'Cart'),
        (TYPE_NEW_USER, 'New user')
    ]
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default=TYPE_PRODUCT)

    # Discount logic
    DISCOUNT_PERCENT = 'percent'
    DISCOUNT_FLAT = 'flat'
    DISCOUNT_TYPE_CHOICES = [
        (DISCOUNT_PERCENT, 'Percentage'),
        (DISCOUNT_FLAT, 'Flat')
    ]
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default=DISCOUNT_PERCENT)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       help_text='Maximum discount amount (optional)')
    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         help_text='Minimum cart value for cart offers')

    # Targeting
    products = models.ManyToManyField('Product', related_name='offers', blank=True)
    categories = models.ManyToManyField('Category', related_name='offers', blank=True)

    # Validity & control
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    # Eligibility
    ELIG_ALL = 'all'
    ELIG_LOGGED_IN = 'logged_in'
    ELIG_NEW = 'new'
    USER_ELIGIBILITY_CHOICES = [
        (ELIG_ALL, 'All users'),
        (ELIG_LOGGED_IN, 'Logged-in users'),
        (ELIG_NEW, 'New users (first order)')
    ]
    user_eligibility = models.CharField(max_length=20, choices=USER_ELIGIBILITY_CHOICES, default=ELIG_ALL)

    # Usage control
    usage_limit_per_user = models.PositiveIntegerField(blank=True, null=True)
    total_usage_limit = models.PositiveIntegerField(blank=True, null=True)
    times_used = models.PositiveIntegerField(default=0)

    # Priority & stacking
    priority = models.IntegerField(default=0, help_text='Higher priority offers are preferred')
    stackable = models.BooleanField(default=False, help_text='Whether this offer can stack with others')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-start_date']

    def __str__(self):
        return f"{self.title} ({self.discount_type} {self.discount_value})"

    def is_currently_active(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        if self.total_usage_limit is not None and self.times_used >= self.total_usage_limit:
            return False
        return True

    def is_applicable(self, *, user=None, cart_total=None, product=None, user_is_new_fn=None):
        """Basic applicability checks. For 'new user' eligibility provide user_is_new_fn(user) -> bool.

        - product: Product instance when checking product/category offers
        - cart_total: Decimal/float for cart offers
        """
        if not self.is_currently_active():
            return False

        # Check min cart value for cart offers
        if self.offer_type == self.TYPE_CART and self.min_cart_value:
            if cart_total is None:
                return False
            try:
                if float(cart_total) < float(self.min_cart_value):
                    return False
            except Exception:
                return False

        # User eligibility
        if self.user_eligibility == self.ELIG_LOGGED_IN and (not user or not getattr(user, 'is_authenticated', False)):
            return False
        if self.user_eligibility == self.ELIG_NEW:
            if not user:
                return False
            if callable(user_is_new_fn):
                try:
                    if not user_is_new_fn(user):
                        return False
                except Exception:
                    return False
            else:
                # No function provided to determine new user status -> cannot assert applicability
                return False

        # Product/category matching
        if self.offer_type == self.TYPE_PRODUCT:
            if not product:
                return False
            if self.products.exists() and product not in self.products.all():
                return False
        if self.offer_type == self.TYPE_CATEGORY:
            if not product:
                return False
            if self.categories.exists():
                if product.category not in self.categories.all():
                    return False

        return True

    def compute_discount(self, *, base_amount, product=None, cart_total=None):
        """Compute discount amount (absolute value) for a given base_amount.
        base_amount: amount to apply discount on (product price or cart total)
        Returns Decimal (float-compatible) representing discount to subtract.
        """
        try:
            amt = float(base_amount)
        except Exception:
            return 0.0

        if self.discount_type == self.DISCOUNT_PERCENT:
            discount = amt * (float(self.discount_value or 0) / 100.0)
        else:
            discount = float(self.discount_value or 0)

        if self.max_discount is not None:
            discount = min(discount, float(self.max_discount))

        # Do not exceed base amount
        discount = min(discount, amt)
        return round(discount, 2)
