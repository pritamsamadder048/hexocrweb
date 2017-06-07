# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 08:43
from __future__ import unicode_literals

from django.db import migrations, models
import hexocrwebapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocr_image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=hexocrwebapp.models.ocr_image_upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(blank=True, default=0, null=True)),
                ('width_field', models.IntegerField(blank=True, default=0, null=True)),
                ('extracted_data', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=40)),
                ('log', models.TextField(blank=True, null=True)),
                ('process_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]