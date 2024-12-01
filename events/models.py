from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    artist_name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)  # Use current time as default
    location = models.CharField(max_length=200)
    source = models.URLField(max_length=200, blank=True, null=True)
    weekly = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically add 'http://' if the source is missing 'http://' or 'https://'
        if self.source and not self.source.startswith(('http://', 'https://')):
            self.source = 'http://' + self.source  # Default to http if neither is present
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        if self.artist_name:
            return f"{self.artist_name} @ {self.title}"
        return self.title


class AdminAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
