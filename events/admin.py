from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Event
from datetime import timedelta

# Action for tagging selected events
def tag_selected_events(modeladmin, request, queryset):
    tag_choices = Event.TAG_CHOICES

    if 'apply' in request.POST:
        selected_tag = request.POST.get('tag')
        if selected_tag:
            valid_tags = dict(Event.TAG_CHOICES).keys()
            if selected_tag in valid_tags:
                for event in queryset:
                    event.tags = selected_tag
                    event.save()
                modeladmin.message_user(request, f"Tag '{selected_tag}' applied to selected events.")
            else:
                modeladmin.message_user(request, "Invalid tag selected.", level="error")
        else:
            modeladmin.message_user(request, "No tag selected.", level="error")
        return

    return render(
        request,
        'admin/tag_selected_events.html',
        {'events': queryset, 'tag_choices': tag_choices, 'title': 'Tag Selected Events'}
    )

tag_selected_events.short_description = "Tag selected events"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist_name', 'date', 'location', 'source', 'tags')
    fields = ('title', 'artist_name', 'location', 'date', 'description', 'source', 'weekly', 'tags')
    actions = [tag_selected_events]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and obj.weekly:
            for week in range(1, 4):
                Event.objects.create(
                    title=obj.title,
                    artist_name=obj.artist_name,
                    location=obj.location,
                    date=obj.date + timedelta(weeks=week),
                    description=obj.description,
                    source=obj.source,
                    tags=obj.tags,
                    weekly=False
                )


# Override the UserAdmin to restrict "Reset Password" and "Password Field"
class UserAdmin(DefaultUserAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser:
            extra_context = extra_context or {}
            extra_context['show_password_reset_button'] = False  # Hide the reset button
        return super().change_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Remove password-related fields for non-superusers
            if 'password' in form.base_fields:
                del form.base_fields['password']
        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            # Remove password fields from the displayed fieldsets for non-superusers
            return [
                (name, {'fields': [field for field in fields if field != 'password']})
                for name, opts in fieldsets
                for fields in (opts.get('fields', []),)
            ]
        return fieldsets

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return False  # Disallow changes to User model for non-superusers
        return super().has_change_permission(request, obj)

# Unregister the default UserAdmin and register the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
