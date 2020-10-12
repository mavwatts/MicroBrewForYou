# Generated by Django 3.1.2 on 2020-10-12 16:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('microbrewforyou_app', '0009_auto_20201008_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='breweries',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='breweries',
            name='state',
            field=models.TextField(default='', max_length=80),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_since',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='breweries',
            name='city',
            field=models.TextField(max_length=80),
        ),
    ]
