from django.db import models
from .validators import file_validator
# Create your models here.
class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISHED = 'PU', 'Published' 
        DRAFT = 'DR', 'Draft'
        UNLISTED = 'UN', 'Unlisted'
        
    title = models.CharField(max_length=220)
    video = models.FileField(upload_to='static/videos', default=False, validators=[file_validator])
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # 'this-is-my-video'
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    # timestamp = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    # publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    objects = models.Manager()


    def __str__(self):
        return str(self.title)

    @property
    def is_published(self):
        return self.active

class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'