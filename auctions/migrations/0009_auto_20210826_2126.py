# Generated by Django 3.2 on 2021-08-26 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_img_url_listing_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='c_bid',
            new_name='current_bid',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='s_bid',
            new_name='starting_bid',
        ),
    ]
