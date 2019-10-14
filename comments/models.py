from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from news_posts.models import NewsPost


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    post = models.ForeignKey(
        NewsPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment by {self.author}'

    def children(self):
        '''
        Returns the children of the comment
        '''
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        '''
        Check if comment is parent
        '''
        if self.parent is not None:
            return False
        else:
            return True
