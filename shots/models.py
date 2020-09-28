from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount


def ShotFilesPath(instance, filename):
    return 'uploads/shots/{0}/{1}'.format(instance.shot.user, filename)


def ShotThumbnailPath(instance, filename):
    return 'uploads/shots/{0}/{1}'.format(instance.user, filename)


class Shot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.TextField(max_length=48, blank=True)
    tags = TaggableManager()
    thumbnail = models.ImageField(
        upload_to=ShotThumbnailPath, blank=False, default='some photo')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=100)
    published = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, null=False)
    hit_count = GenericRelation(HitCount, object_id_field='object_p',
                                related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Shot, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.is_published)


class ShotsFile(models.Model):
    file = models.ImageField(upload_to=ShotFilesPath, blank=False)
    shot = models.ForeignKey(Shot, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.shot.user) + ' - ' + str(self.shot.title)
