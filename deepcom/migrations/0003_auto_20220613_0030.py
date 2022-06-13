# Generated by Django 3.1.12 on 2022-06-12 23:30

import deepcom.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('deepcom', '0002_processedvideo_delete_particledata'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True)),
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('video_path', models.CharField(max_length=255)),
                ('frames', djongo.models.fields.ArrayField(model_container=deepcom.models.Frame, model_form_class=deepcom.models.FrameForm)),
            ],
        ),
        migrations.DeleteModel(
            name='ProcessedVideo',
        ),
    ]