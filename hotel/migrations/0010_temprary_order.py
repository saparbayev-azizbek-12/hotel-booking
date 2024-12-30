# Generated by Django 5.1.4 on 2024-12-16 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0009_facilities_stars'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temprary_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('adults', models.CharField(choices=[('Adult', 'Adult'), ('1 Adult', '1 Adult'), ('2 Adult', '2 Adult'), ('3 Adult', '3 Adult'), ('4 Adult', '4 Adult'), ('5 Adult', '5 Adult')], max_length=15)),
                ('children', models.CharField(choices=[('Children', 'Children'), ('1 Child', '1 Child'), ('2 Children', '2 Children'), ('3 Children', '3 Children'), ('4 Children', '4 Children'), ('5 Children', '5 Children')], max_length=20)),
            ],
        ),
    ]
