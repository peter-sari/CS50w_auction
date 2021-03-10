# Generated by Django 3.1.6 on 2021-03-03 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210303_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='listingID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing', verbose_name='Listing item'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]