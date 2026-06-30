from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class GuideProfile(models.Model):
    CATEGORY_CHOICES = [
        ('cultural', 'Cultural'),
        ('historical', 'Historical'),
        ('nature', 'Nature & Wildlife'),
        ('adventure', 'Adventure'),
        ('food', 'Food & Cuisine'),
        ('religious', 'Religious & Spiritual'),
        ('general', 'General'),
    ]

    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('hausa', 'Hausa'),
        ('yoruba', 'Yoruba'),
        ('igbo', 'Igbo'),
        ('pidgin', 'Nigerian Pidgin'),
        ('french', 'French'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guideprofile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    years_of_experience = models.PositiveIntegerField(default=0)
    languages = models.CharField(max_length=200, blank=True, help_text='Comma-separated list of languages spoken')
    profile_photo = models.ImageField(upload_to='guide_photos/', blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} — Guide Profile"

    def update_average_rating(self):
        from reviews.models import Review
        from django.db.models import Avg
        avg = Review.objects.filter(guide=self.user).aggregate(Avg('rating'))['rating__avg']
        self.average_rating = round(avg, 1) if avg else 0.0
        self.save(update_fields=['average_rating'])

    @property
    def languages_list(self):
        return [lang.strip() for lang in self.languages.split(',') if lang.strip()]

    @property
    def active_experiences(self):
        return self.experiences.filter(is_active=True)


class Experience(models.Model):
    CATEGORY_CHOICES = GuideProfile.CATEGORY_CHOICES

    guide = models.ForeignKey(GuideProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0.5)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.guide.user.get_full_name()}"
