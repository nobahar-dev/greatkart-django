# Generated by Django 5.0.1 on 2024-01-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
