# Generated by Django 3.1.2 on 2020-10-16 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microbrewforyou_app', '0010_auto_20201012_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewtypes',
            name='img_upload',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
