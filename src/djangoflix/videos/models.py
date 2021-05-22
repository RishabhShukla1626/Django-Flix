from django.db import models
from .validators import file_validator
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.

class PublishStateOptions(models.TextChoices):
        PUBLISHED = 'PU', 'Published' 
        DRAFT = 'DR', 'Draft'
        UNLISTED = 'UN', 'Unlisted'

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=Video.videostateoptions.PUBLISHED,publish_timestamp__lte=now)

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    def published(self):
        return self.get_queryset().published()

class Video(models.Model):
    
    videostateoptions = PublishStateOptions
    title = models.CharField(max_length=220)
    video = models.FileField(upload_to='static/videos', default=False, validators=[file_validator])
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # 'this-is-my-video'
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=videostateoptions.choices, default=videostateoptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    
    objects = VideoManager()


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

def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_published = instance.state == PublishStateOptions.PUBLISHED
    is_draft = instance.state == PublishStateOptions.DRAFT
    if is_published and instance.publish_timestamp is None:
        print("save as timestamp for published")
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None

pre_save.connect(publish_state_pre_save, sender=Video)

def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug == None:
        instance.slug = slugify(title)

pre_save.connect(slugify_pre_save, sender=Video)