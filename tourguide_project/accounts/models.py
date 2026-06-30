from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_TOURIST = 'tourist'
    ROLE_GUIDE = 'guide'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_TOURIST, 'Tourist'),
        (ROLE_GUIDE, 'Tour Guide'),
        (ROLE_ADMIN, 'Administrator'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_TOURIST)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_tourist(self):
        return self.role == self.ROLE_TOURIST

    @property
    def is_guide(self):
        return self.role == self.ROLE_GUIDE

    @property
    def is_platform_admin(self):
        return self.role == self.ROLE_ADMIN


@receiver(post_save, sender=User)
def create_guide_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.ROLE_GUIDE:
        from guides.models import GuideProfile
        GuideProfile.objects.get_or_create(user=instance)
