# Generated by Django 5.1.3 on 2024-12-01 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='artist_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
