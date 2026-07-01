from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from .models import GuideProfile, Experience
from .forms import GuideProfileForm, ExperienceForm, GuideSearchForm


def guide_list(request):
    form = GuideSearchForm(request.GET or None)
    profiles = GuideProfile.objects.filter(is_verified=True).select_related('user')
    
    # print(f"DEBUG: Total verified profiles found : {profiles.count()}")
    # if q:
    #     profiles = profiles.filter(...)
    #     print(f"DEBUG: Profiles after search query: {profiles.count()}")

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    language = request.GET.get('language', '')
    min_rating = request.GET.get('min_rating', '')

    if q:
        profiles = profiles.filter(
            Q(location__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(bio__icontains=q)
        )
    if category:
        profiles = profiles.filter(specialization__icontains=category)
    if language:
        profiles = profiles.filter(languages__icontains=language)
    if min_rating:
        profiles = profiles.filter(average_rating__gte=float(min_rating))

    profiles = profiles.order_by('-average_rating', '-is_verified')
    per_page = getattr(settings, 'GUIDES_PER_PAGE', 12)
    paginator = Paginator(profiles, per_page)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'guides/guide_list.html', {
        'form': form,
        'page_obj': page_obj,
        'query_string': request.GET.urlencode(),
    })


def guide_detail(request, pk):
    profile = get_object_or_404(GuideProfile, pk=pk)
    experiences = profile.experiences.filter(is_active=True)
    from reviews.models import Review
    reviews = Review.objects.filter(guide=profile.user).select_related('tourist').order_by('-created_at')
    return render(request, 'guides/guide_detail.html', {
        'profile': profile,
        'experiences': experiences,
        'reviews': reviews,
    })


@login_required
def profile_edit(request):
    if not request.user.is_guide:
        messages.error(request, 'Only tour guides can access this page.')
        return redirect('accounts:dashboard')
    profile, _ = GuideProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = GuideProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('guides:guide_detail', pk=profile.pk)
    else:
        form = GuideProfileForm(instance=profile)
    return render(request, 'guides/profile_edit.html', {'form': form, 'profile': profile})


@login_required
def experience_create(request):
    if not request.user.is_guide:
        messages.error(request, 'Only tour guides can create experiences.')
        return redirect('accounts:dashboard')
    profile = get_object_or_404(GuideProfile, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.guide = profile
            experience.save()
            messages.success(request, f'Experience "{experience.title}" created successfully.')
            return redirect('guides:guide_detail', pk=profile.pk)
    else:
        form = ExperienceForm()
    return render(request, 'guides/experience_form.html', {'form': form, 'action': 'Create'})


@login_required
def experience_edit(request, pk):
    profile = get_object_or_404(GuideProfile, user=request.user)
    experience = get_object_or_404(Experience, pk=pk, guide=profile)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, f'Experience "{experience.title}" updated.')
            return redirect('guides:guide_detail', pk=profile.pk)
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'guides/experience_form.html', {'form': form, 'action': 'Edit', 'experience': experience})


@login_required
def experience_delete(request, pk):
    profile = get_object_or_404(GuideProfile, user=request.user)
    experience = get_object_or_404(Experience, pk=pk, guide=profile)
    if request.method == 'POST':
        title = experience.title
        experience.delete()
        messages.success(request, f'Experience "{title}" has been deleted.')
        return redirect('guides:guide_detail', pk=profile.pk)
    return render(request, 'guides/experience_confirm_delete.html', {'experience': experience})
