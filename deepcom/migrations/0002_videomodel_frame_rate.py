# Generated by Django 3.1.12 on 2024-06-20 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepcom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='frame_rate',
            field=models.FloatField(null=True),
        ),
    ]
