from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from datetime import datetime



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status = 'published')


class Comments(models.Model):
    pass

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
    author = models.ForeignKey(User, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = datetime.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10,
        choices = STATUS_CHOICES,
        default = 'draft'
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        url_pattern = reverse('blog:post_detail_view',
                        args = [
                            self.publish.year,
                            self.publish.strftime('%m'),
                            self.publish.strftime('%d'),
                            self.slug
                        ]
                    )


        return url_pattern

    def __str__(self):
        return self.title
