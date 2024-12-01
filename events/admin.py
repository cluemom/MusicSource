from django.contrib import admin
from .models import Event, AdminAccount
from django.utils.timezone import timedelta


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'source')
    fields = ('title', 'artist_name', 'location', 'date', 'description', 'source', 'weekly')  # Added 'weekly' field to the form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Automatically populate 4 weeks' worth of events if 'weekly' is checked
        if not change and obj.weekly:
            for week in range(1, 4):  # Generate events for the next 3 weeks
                Event.objects.create(
                    title=obj.title,
                    artist_name=obj.artist_name,  # Include artist name for new events
                    location=obj.location,
                    date=obj.date + timedelta(weeks=week),
                    description=obj.description,
                    source=obj.source,
                    weekly=False  # Prevent recursion
                )


@admin.register(AdminAccount)
class AdminAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
