from django.shortcuts import render, get_object_or_404
from .models import Event
from django.utils.timezone import now

def events_list(request):
    events = Event.objects.filter(date__gte=now()).order_by('date')
    return render(request, 'events/events_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})