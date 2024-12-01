from django.core.management.base import BaseCommand
from events.models import Event
from events.utils import fetch_facebook_events

class Command(BaseCommand):
    # todo:finish this
    help = 'Import Facebook events'

    def handle(self, *args, **kwargs):
        access_token = 'YOUR_FACEBOOK_ACCESS_TOKEN'
        page_id = 'YOUR_PAGE_ID'
        events = fetch_facebook_events(access_token, page_id)
        for fb_event in events:
            Event.objects.create(
                title=fb_event['name'],
                description=fb_event.get('description', ''),
                date=fb_event['start_time'][:10],
                time=fb_event['start_time'][11:16],
                location=fb_event.get('place', {}).get('name', ''),
                source='Facebook'
            )
        self.stdout.write('Successfully imported Facebook events.')
