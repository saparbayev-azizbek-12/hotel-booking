# Generated by Django 5.1.4 on 2024-12-16 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_alter_room_price_per_night'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilities',
            name='room',
            field=models.ForeignKey(default=0.00037055335968379444, on_delete=django.db.models.deletion.CASCADE, to='hotel.room'),
            preserve_default=False,
        ),
    ]