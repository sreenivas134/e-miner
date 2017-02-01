from django.db import models
from django_markdown.models import MarkdownField
from django.template.defaultfilters import slugify
# Create your models here.

class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        return self.slug

class NewEntry(models.Model):
    title = models.CharField(max_length=200,)
    body = MarkdownField()
    published = models.BooleanField(default=False)
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length = 200,)
    tag = models.ManyToManyField(Tag, null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title).__str__()
        super(NewEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title