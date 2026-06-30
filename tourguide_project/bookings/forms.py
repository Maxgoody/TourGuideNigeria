from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['requested_date', 'notes']
        widgets = {
            'requested_date': forms.DateInput(attrs={'type': 'date', 'min': str(timezone.now().date())}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests or questions for the guide?'}),
        }

    def clean_requested_date(self):
        date = self.cleaned_data.get('requested_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError('Please select a future date.')
        return date
