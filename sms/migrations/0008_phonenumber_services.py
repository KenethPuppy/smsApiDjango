# Generated by Django 4.2.2 on 2023-06-17 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0007_remove_phonenumber_vk'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='services',
            field=models.JSONField(default=None),
        ),
    ]