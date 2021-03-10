# Generated by Django 3.1.6 on 2021-03-10 09:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20210310_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='listingWinner',
        ),
        migrations.AddField(
            model_name='listing',
            name='listingWinner',
            field=models.ManyToManyField(blank=True, related_name='listingWinner', to=settings.AUTH_USER_MODEL, verbose_name='Winner'),
        ),
    ]
