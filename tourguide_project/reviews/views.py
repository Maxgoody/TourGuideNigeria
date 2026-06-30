from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .models import Review
from .forms import ReviewForm


@login_required
def review_create(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk)

    # Access control checks
    if booking.tourist != request.user:
        messages.error(request, 'You can only review your own bookings.')
        return redirect('bookings:booking_list')
    if booking.status != Booking.STATUS_COMPLETED:
        messages.error(request, 'You can only review completed bookings.')
        return redirect('bookings:booking_list')
    if hasattr(booking, 'review'):
        messages.info(request, 'You have already submitted a review for this booking.')
        return redirect('bookings:booking_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.tourist = request.user
            review.guide = booking.guide
            review.save()
            messages.success(request, 'Your review has been submitted. Thank you!')
            return redirect('guides:guide_detail', pk=booking.guide.guideprofile.pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {
        'form': form,
        'booking': booking,
    })
