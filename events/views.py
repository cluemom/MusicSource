from django.shortcuts import render, get_object_or_404
from .models import Event
from django.utils.timezone import now, localtime
from datetime import timedelta, date
import calendar

def events_list(request):
    tag_filter = request.GET.get('tag')
    hide_open_mic = 'hide_open_mic' in request.GET
    month = int(request.GET.get('month', now().month))
    year = int(request.GET.get('year', now().year))

    # Current, previous, and next months
    current_date = date(year, month, 1)
    next_month_date = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
    prev_month_date = (current_date - timedelta(days=1)).replace(day=1)

    # Check if the previous month navigation is needed
    has_previous_month = current_date > localtime(now()).date().replace(day=1)

    # Filter events
    events = Event.objects.filter(
        date__gte=now(),
        date__month=month,
        date__year=year
    ).order_by('date')
    if tag_filter:
        events = events.filter(tags=tag_filter)
    if hide_open_mic:
        events = events.exclude(tags="open_mic")

    # Normalize today's date to America/Chicago time
    today = localtime(now()).date()

    context = {
        'events': events,
        'current_month_name': calendar.month_name[current_date.month],
        'current_year': current_date.year,
        'next_month_name': calendar.month_name[next_month_date.month],
        'next_month': next_month_date.month,
        'next_year': next_month_date.year,
        'has_previous_month': has_previous_month,
        'prev_month_name': calendar.month_name[prev_month_date.month],
        'prev_month': prev_month_date.month,
        'prev_year': prev_month_date.year,
        'hide_open_mic': hide_open_mic,
        'today': today,  # Pass normalized today
    }
    return render(request, 'events/events_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.date < now():
        raise Http404("This event has passed.")
    return render(request, 'events/event_detail.html', {'event': event})
