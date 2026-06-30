from django import forms
from .models import GuideProfile, Experience


class GuideProfileForm(forms.ModelForm):
    class Meta:
        model = GuideProfile
        fields = ['bio', 'location', 'specialization', 'years_of_experience', 'languages', 'profile_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell tourists about yourself, your expertise, and what makes your tours special...'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Lagos, Abuja, Kano'}),
            'languages': forms.TextInput(attrs={'placeholder': 'e.g. English, Yoruba, Hausa'}),
            'years_of_experience': forms.NumberInput(attrs={'min': 0}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description', 'category', 'duration_hours', 'price', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Lagos Heritage Walking Tour'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe what tourists will see, do, and experience...'}),
            'duration_hours': forms.NumberInput(attrs={'min': 0.5, 'step': 0.5, 'placeholder': 'e.g. 3.0'}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'placeholder': 'Price per person in NGN'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Victoria Island, Lagos'}),
        }


class GuideSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Location or keyword',
                        widget=forms.TextInput(attrs={'placeholder': 'Search by location or name...'}))
    category = forms.ChoiceField(required=False, choices=[('', 'All Categories')] + GuideProfile.CATEGORY_CHOICES)
    language = forms.ChoiceField(required=False, choices=[('', 'Any Language')] + GuideProfile.LANGUAGE_CHOICES)
    min_rating = forms.ChoiceField(required=False, label='Minimum Rating', choices=[
        ('', 'Any Rating'), ('1', '1+'), ('2', '2+'), ('3', '3+'), ('4', '4+'), ('5', '5 only'),
    ])
