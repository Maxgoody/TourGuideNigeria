from django.contrib import admin
from .models import GuideProfile, Experience


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'specialization', 'average_rating', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'specialization']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'location']
    readonly_fields = ['average_rating', 'created_at', 'updated_at']
    actions = ['verify_profiles', 'unverify_profiles']

    @admin.action(description='Mark selected profiles as verified')
    def verify_profiles(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} profile(s) marked as verified.')

    @admin.action(description='Remove verification from selected profiles')
    def unverify_profiles(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} profile(s) unverified.')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'guide', 'category', 'price', 'duration_hours', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'guide__user__first_name', 'guide__user__last_name', 'location']
    actions = ['activate_experiences', 'deactivate_experiences']

    @admin.action(description='Activate selected experiences')
    def activate_experiences(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected experiences')
    def deactivate_experiences(self, request, queryset):
        queryset.update(is_active=False)
