# Generated by Django 3.1.12 on 2022-06-30 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepcom', '0002_auto_20220630_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processingparametersmodel',
            name='video_linked',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
