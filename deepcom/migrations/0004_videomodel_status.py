# Generated by Django 3.1.12 on 2022-06-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepcom', '0003_auto_20220613_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='status',
            field=models.CharField(default='UNPROCESSED', max_length=255),
        ),
    ]
