from django.db import models
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage


class Video(models.Model):
    SOURCE_YOUTUBE = 'youtube'
    SOURCE_FILE = 'file'
    SOURCE_CHOICES = [
        (SOURCE_YOUTUBE, 'YouTube (embed URL)'),
        (SOURCE_FILE, 'Uploaded file')
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    source = models.CharField(max_length=16, choices=SOURCE_CHOICES, default=SOURCE_YOUTUBE)
    embed_url = models.CharField(max_length=1024, blank=True, help_text='YouTube embed URL, e.g. https://www.youtube.com/embed/...')
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, storage=VideoMediaCloudinaryStorage())
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, storage=MediaCloudinaryStorage())
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)
