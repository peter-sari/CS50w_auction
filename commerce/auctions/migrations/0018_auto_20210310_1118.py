# Generated by Django 3.1.6 on 2021-03-10 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20210310_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watchers', to=settings.AUTH_USER_MODEL, verbose_name='Watchers'),
        ),
    ]
