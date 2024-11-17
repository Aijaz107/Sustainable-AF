# Generated by Django 5.1.2 on 2024-11-13 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('bio', models.TextField(blank=True, null=True)),
                ('user_type', models.CharField(choices=[('NGO', 'NGO'), ('Corporation', 'Corporation'), ('Individual', 'Individual')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userregistration'),
        ),
        migrations.AlterField(
            model_name='partnership',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='app.userregistration'),
        ),
        migrations.AlterField(
            model_name='partnership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partnerships', to='app.userregistration'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userregistration'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
