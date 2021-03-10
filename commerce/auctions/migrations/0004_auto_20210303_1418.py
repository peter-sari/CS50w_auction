# Generated by Django 3.1.6 on 2021-03-03 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210303_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listingCategory',
            field=models.CharField(choices=[('fashion', 'fashion'), ('electronics', 'electronics'), ('sports', 'sports'), ('home', 'home'), ('motors', 'motors'), ('art', 'art'), ('business', 'business'), ('media', 'media'), ('others', 'others')], default='others', max_length=64),
        ),
        migrations.AddField(
            model_name='listing',
            name='listingFirstBid',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='listing',
            name='listingImage',
            field=models.URLField(blank=True),
        ),
    ]
