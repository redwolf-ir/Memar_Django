from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='uploads/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_premium = models.BooleanField(default=False, null=False)
    birth_date = models.DateField(null=True, blank=True)
    location = models.TextField(max_length=100, blank=True)
    website = models.TextField(max_length=45, blank=True)
    twitter = models.TextField(max_length=16, blank=True)
    facebook = models.TextField(max_length=16, blank=True)
    instagram = models.TextField(max_length=16, blank=True)
    github = models.TextField(max_length=16, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.user)


class Passwordresetcodes(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=100, blank=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '--{}-- Password Reset Request'.format(self.user)
