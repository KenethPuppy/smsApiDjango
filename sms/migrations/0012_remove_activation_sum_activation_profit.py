# Generated by Django 4.2.2 on 2023-06-19 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0011_activation_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activation',
            name='sum',
        ),
        migrations.AddField(
            model_name='activation',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Доход'),
        ),
    ]