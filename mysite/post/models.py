from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.TextField(max_length=30)
    email = models.TextField(max_length=60)
    email_confirmed = models.BooleanField(default=False)

    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)
    # country = models.CharField(max_length=30, blank=True)
    # city = models.CharField(max_length=30, blank=True)

    # def __str__(self):
    #     return u'user: %s, email_confirmed: %s' % (self.user, self.email_confirmed)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
