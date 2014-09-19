import os
import datetime

from django.db import models
from django.utils.text import slugify

from tinymce import models as tinymce_models


################################################################################
# UPLOAD FUNCTIONS USED BY MODELS
################################################################################

def now():
    '''
    Returns number of microseconds since Jan. 1, 2014 as a unicode string
    '''
    now = int((datetime.datetime.utcnow() -
               datetime.datetime(2014, 1, 1)).total_seconds() * (10 ** 6))
    return unicode(now)


def issue_upload_to(instance, filename):
    '''
    Returns the filepath to which an issue's cover image should be uploaded
    '''
    # Remove any characters that are not alphanumeric or a dot
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])

    # return issue_covers/<issue_name>/<now()>_<fname>
    return os.path.join('issue_covers', str(instance.pub_date.year),
                        slugify(instance.name), now() + '_' + fname)


def upload_image_to(instance, filename):
    '''
    Returns the filepath to which an Image's image should be uploaded
    '''
    # Remove any characters that are not alphanumeric or a dot
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])

    # return images/<issue_name>/<issue_name>/<now()>_<fname>
    return os.path.join('images', slugify(instance.issue.name),
                        now() + '_' + fname)


def upload_article_image_to(instance, filename):
    '''
    Returns the filepath to which an Image associated with an Article should be
    uploaded
    '''
    # Remove any characters that are not alphanumeric or a dot
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])

    # return article_images/<issue_name>/<issue_name>/<now()>_<fname>
    return os.path.join('article_images', slugify(instance.issue.name),
                        now() + '_' + fname)


################################################################################
# ACTUAL MODELS
################################################################################

class Issue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    pub_date = models.DateField()
    cover_image = models.ImageField(upload_to=issue_upload_to, blank=True,
                                    null=True)

    def __unicode__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Contributor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    teaser = models.TextField()
    body = tinymce_models.HTMLField()
    is_featured = models.BooleanField(default=False)

    # Legacy fields; we should probably get rid of this eventually
    medium = tinymce_models.HTMLField()
    size = tinymce_models.HTMLField()
    statement = tinymce_models.HTMLField()

    issue = models.ForeignKey('Issue')
    section = models.ForeignKey('Section')
    contributors = models.ManyToManyField(Contributor)
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        super(Content, self).save(*args, **kwargs)

        # Unfeature all other featured pieces of content if this one is featured
        if self.is_featured:
            featured = type(self).objects.filter(
                issue=self.issue, section=self.section,
                is_featured=True).exclude(
                    pk=self.pk)
            for c in featured:
                c.is_featured = False
                c.save()

    def __unicode__(self):
        return self.title


class Image(Content):
    photo = models.ImageField(upload_to=upload_image_to)


class Article(Content):
    related_image = models.ImageField(upload_to=upload_article_image_to,
                                      null=True, default=None)
