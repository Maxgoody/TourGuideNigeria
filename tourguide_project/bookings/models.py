from django.db import models
from django.conf import settings
from django.utils import timezone


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings_as_tourist')
    guide = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings_as_guide')
    experience = models.ForeignKey('guides.Experience', on_delete=models.CASCADE, related_name='bookings')
    requested_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} — {self.tourist.get_full_name()} → {self.guide.get_full_name()} on {self.requested_date}"

    @property
    def can_be_reviewed(self):
        return self.status == self.STATUS_COMPLETED and not hasattr(self, 'review')

    @property
    def has_review(self):
        return hasattr(self, 'review')

    @property
    def status_badge_class(self):
        return {
            self.STATUS_PENDING: 'warning',
            self.STATUS_CONFIRMED: 'primary',
            self.STATUS_COMPLETED: 'success',
            self.STATUS_CANCELLED: 'danger',
        }.get(self.status, 'secondary')
