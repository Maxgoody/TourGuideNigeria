from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourist', 'guide', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['tourist__email', 'guide__email', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    actions = ['delete_flagged']

    @admin.action(description='Delete selected reviews')
    def delete_flagged(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} review(s) deleted.')
