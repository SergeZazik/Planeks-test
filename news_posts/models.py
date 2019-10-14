from django.conf import settings
from django.db import models
from django.urls import reverse
from .validators import validate_file_extensions
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


def upload_file_location(instance, filename):
    """
    Returns a relative location of uploaded media files
    """
    return f'{instance.slug}/{filename}'


class NewsPost(models.Model):
    """
    Model for News post
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField(max_length=500)
    attachment = models.FileField(
        validators=[validate_file_extensions],
        upload_to=upload_file_location,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns an absolute url to a news post
        """
        return reverse('news_posts:news_post_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created', '-updated']


@receiver(pre_save, sender=NewsPost)
def auto_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title, allow_unicode=True)


@receiver(post_delete, sender=NewsPost)
def delete_files(sender, instance, *args, **kwargs):
    instance.attachment.delete(False)

