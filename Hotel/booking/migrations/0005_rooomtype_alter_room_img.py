# Generated by Django 4.2.4 on 2023-08-04 09:26

import booking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_room_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='RooomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Special', 'Special'), ('General', 'General')], max_length=10)),
                ('capacity', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')], max_length=10)),
                ('ideal_for', models.CharField(choices=[('Human', 'Human'), ('Monster', 'Monster')], max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='img',
            field=models.ImageField(upload_to=booking.models.get_room_image_upload_path),
        ),
    ]
