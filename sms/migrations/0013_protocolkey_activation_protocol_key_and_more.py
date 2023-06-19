# Generated by Django 4.2.2 on 2023-06-19 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0012_remove_activation_sum_activation_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtocolKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='activation',
            name='protocol_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='sms.protocolkey'),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='protocol_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='sms.protocolkey'),
        ),
        migrations.AddField(
            model_name='sms',
            name='protocol_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='sms.protocolkey'),
        ),
    ]
