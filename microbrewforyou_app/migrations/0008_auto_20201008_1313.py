# Generated by Django 3.1.2 on 2020-10-08 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microbrewforyou_app', '0007_auto_20201007_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='fav_brewtypes',
        ),
        migrations.AddField(
            model_name='customuser',
            name='fav_brewtypes',
            field=models.ManyToManyField(blank=True, null=True, related_name='fav_brewtypes', to='microbrewforyou_app.BrewTypes'),
        ),
    ]