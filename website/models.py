from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField


def banner_upload_to(instance, filename):
    # store banners under media/banners/<filename>
    return f'banners/{filename}'


from cloudinary_storage.storage import MediaCloudinaryStorage

class Banner(models.Model):
    title = models.CharField(_('title'), max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/', storage=MediaCloudinaryStorage())
    alt_text = models.CharField(_('alt text'), max_length=255, blank=True)
    link = models.URLField(_('link'), blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    # slot determines where the banner will be used: hero area or mini slider
    SLOT_HERO = 'hero'
    SLOT_MINI = 'mini'
    SLOT_CHOICES = [
        (SLOT_HERO, 'Hero'),
        (SLOT_MINI, 'Mini Slider'),
    ]
    slot = models.CharField(_('slot'), max_length=10, choices=SLOT_CHOICES, default=SLOT_HERO, help_text=_('Where this banner is used'))
    order = models.PositiveIntegerField(_('order'), default=0, help_text=_('Lower numbers appear first'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _('banner')
        verbose_name_plural = _('banners')

    def __str__(self):
        return self.title or f'Banner #{self.pk}'


class FeedType(models.Model):
    title = models.CharField(_('title'), max_length=100)
    image = models.ImageField(upload_to='feed_types/', storage=MediaCloudinaryStorage())
    description = models.TextField(_('description'))
    protein_content = models.CharField(_('protein content'), max_length=50, blank=True)
    features = models.CharField(_('features'), max_length=255, help_text=_('Comma separated features, e.g. Growth Focus, Milk Booster'))
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('feed type')
        verbose_name_plural = _('feed types')

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]
