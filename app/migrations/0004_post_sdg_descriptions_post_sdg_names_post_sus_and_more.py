# Generated by Django 5.0.3 on 2024-11-20 06:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sdg_descriptions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='post',
            name='sdg_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='post',
            name='sus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='sustainability_dimensions',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='post',
            name='target_descriptions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='post',
            name='target_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, size=None),
        ),
    ]
