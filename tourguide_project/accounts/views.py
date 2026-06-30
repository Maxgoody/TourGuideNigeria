from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TouristRegistrationForm, GuideRegistrationForm, CustomLoginForm
from bookings.models import Booking


def home(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'home.html')


def register_tourist(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = TouristRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your tourist account has been created.')
            return redirect('accounts:dashboard')
    else:
        form = TouristRegistrationForm()
    return render(request, 'accounts/register_tourist.html', {'form': form})


def register_guide(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = GuideRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Please complete your guide profile.')
            return redirect('guides:profile_edit')
    else:
        form = GuideRegistrationForm()
    return render(request, 'accounts/register_guide.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('accounts:dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    user = request.user
    if user.is_guide:
        from guides.models import GuideProfile
        try:
            profile = user.guideprofile
        except GuideProfile.DoesNotExist:
            profile = None
        pending = Booking.objects.filter(guide=user, status=Booking.STATUS_PENDING).count()
        confirmed = Booking.objects.filter(guide=user, status=Booking.STATUS_CONFIRMED).count()
        completed = Booking.objects.filter(guide=user, status=Booking.STATUS_COMPLETED).count()
        context = {
            'profile': profile,
            'pending_count': pending,
            'confirmed_count': confirmed,
            'completed_count': completed,
        }
        return render(request, 'accounts/dashboard_guide.html', context)
    elif user.is_tourist:
        upcoming = Booking.objects.filter(tourist=user, status__in=[
            Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED
        ]).select_related('experience', 'guide').order_by('requested_date')[:5]
        completed = Booking.objects.filter(tourist=user, status=Booking.STATUS_COMPLETED).select_related(
            'experience', 'guide'
        ).order_by('-requested_date')[:5]
        context = {
            'upcoming_bookings': upcoming,
            'completed_bookings': completed,
        }
        return render(request, 'accounts/dashboard_tourist.html', context)
    return redirect('admin:index')
