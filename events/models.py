from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    TAG_CHOICES = [
        ('open_mic', 'Open Mic/Karaoke'),
        ('none', 'Other'),  # Default
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    artist_name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)  # Use current time as default
    location = models.CharField(max_length=200)
    source = models.URLField(max_length=200, blank=True, null=True)
    weekly = models.BooleanField(default=False)
    tags = models.CharField(max_length=20, choices=TAG_CHOICES, default='none')

    def save(self, *args, **kwargs):
        # Automatically add 'http://' if the source is missing 'http://' or 'https://'
        if self.source and not self.source.lower().startswith(('http://', 'https://')):
            self.source = 'http://' + self.source
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        if self.artist_name:
            return f"{self.artist_name} @ {self.title}"
        return self.title

# AdminAccount model (no changes, but marked for deletion as per comment)
class AdminAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
