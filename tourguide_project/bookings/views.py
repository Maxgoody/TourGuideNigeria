from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from guides.models import Experience, GuideProfile
from .models import Booking
from .forms import BookingForm


@login_required
def booking_create(request, experience_pk):
    if not request.user.is_tourist:
        messages.error(request, 'Only tourists can make bookings.')
        return redirect('accounts:dashboard')

    experience = get_object_or_404(Experience, pk=experience_pk, is_active=True)
    guide_user = experience.guide.user

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            requested_date = form.cleaned_data['requested_date']
            # Check for date conflict
            conflict = Booking.objects.filter(
                guide=guide_user,
                requested_date=requested_date,
                status=Booking.STATUS_CONFIRMED
            ).exists()
            if conflict:
                form.add_error('requested_date', 'This guide is not available on the selected date. Please choose another date.')
            else:
                booking = form.save(commit=False)
                booking.tourist = request.user
                booking.guide = guide_user
                booking.experience = experience
                booking.save()
                messages.success(request, 'Your booking request has been submitted! The guide will review it shortly.')
                return redirect('bookings:booking_list')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'experience': experience,
    })


@login_required
def booking_list(request):
    user = request.user
    if user.is_tourist:
        bookings = Booking.objects.filter(tourist=user).select_related('experience', 'guide').prefetch_related('review')
        return render(request, 'bookings/booking_list_tourist.html', {'bookings': bookings})
    elif user.is_guide:
        pending = Booking.objects.filter(guide=user, status=Booking.STATUS_PENDING).select_related('experience', 'tourist')
        confirmed = Booking.objects.filter(guide=user, status=Booking.STATUS_CONFIRMED).select_related('experience', 'tourist')
        completed = Booking.objects.filter(guide=user, status=Booking.STATUS_COMPLETED).select_related('experience', 'tourist').prefetch_related('review')
        cancelled = Booking.objects.filter(guide=user, status=Booking.STATUS_CANCELLED).select_related('experience', 'tourist')
        return render(request, 'bookings/booking_list_guide.html', {
            'pending': pending,
            'confirmed': confirmed,
            'completed': completed,
            'cancelled': cancelled,
        })
    return redirect('accounts:dashboard')


@login_required
def booking_accept(request, pk):
    booking = get_object_or_404(Booking, pk=pk, guide=request.user, status=Booking.STATUS_PENDING)
    if request.method == 'POST':
        booking.status = Booking.STATUS_CONFIRMED
        booking.save()
        messages.success(request, f'Booking from {booking.tourist.get_full_name()} on {booking.requested_date} has been confirmed.')
    return redirect('bookings:booking_list')


@login_required
def booking_decline(request, pk):
    booking = get_object_or_404(Booking, pk=pk, guide=request.user, status=Booking.STATUS_PENDING)
    if request.method == 'POST':
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        messages.info(request, f'Booking from {booking.tourist.get_full_name()} has been declined.')
    return redirect('bookings:booking_list')


@login_required
def booking_complete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, guide=request.user, status=Booking.STATUS_CONFIRMED)
    if request.method == 'POST':
        booking.status = Booking.STATUS_COMPLETED
        booking.save()
        messages.success(request, f'Booking marked as completed. The tourist can now leave a review.')
    return redirect('bookings:booking_list')


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, tourist=request.user, status__in=[
        Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED
    ])
    if request.method == 'POST':
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        messages.info(request, 'Your booking has been cancelled.')
    return redirect('bookings:booking_list')
