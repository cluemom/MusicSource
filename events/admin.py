from django.contrib import admin
from django.shortcuts import render
from .models import Event, AdminAccount
from datetime import timedelta


# Action for tagging selected events
def tag_selected_events(modeladmin, request, queryset):
    # Get the tag choices from the Event model
    tag_choices = Event.TAG_CHOICES

    if 'apply' in request.POST:
        selected_tag = request.POST.get('tag')
        if selected_tag:
            for event in queryset:
                # Update the tags field with the selected choice
                event.tags = selected_tag
                event.save()
            modeladmin.message_user(request, f"Tag '{selected_tag}' applied to selected events.")
            return

    # Render the admin action page with available tag choices
    return render(
        request,
        'admin/tag_selected_events.html',
        {'events': queryset, 'tag_choices': tag_choices, 'title': 'Tag Selected Events'}
    )


tag_selected_events.short_description = "Tag selected events"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'source', 'tags')
    fields = ('title', 'artist_name', 'location', 'date', 'description', 'source', 'weekly', 'tags')
    actions = [tag_selected_events]  # Add the custom action to the actions dropdown

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Automatically populate 4 weeks' worth of events if 'weekly' is checked
        if not change and obj.weekly:  # Only execute on creation
            for week in range(1, 4):  # Generate events for the next 3 weeks
                Event.objects.create(
                    title=obj.title,
                    artist_name=obj.artist_name,
                    location=obj.location,
                    date=obj.date + timedelta(weeks=week),
                    description=obj.description,
                    source=obj.source,
                    tags=obj.tags,
                    weekly=False  # Prevent recursion
                )


@admin.register(AdminAccount)
class AdminAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
